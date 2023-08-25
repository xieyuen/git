import locale
import os
import time
import traceback
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from threading import Lock, Condition
from typing import Optional, Callable, Any, List

import pkg_resources
import psutil
from ruamel.yaml import YAMLError

from mcdreforged.command.command_manager import CommandManager
from mcdreforged.constants import core_constant
from mcdreforged.executor.console_handler import ConsoleHandler
from mcdreforged.executor.task_executor import TaskExecutor
from mcdreforged.executor.update_helper import UpdateHelper
from mcdreforged.executor.watchdog import WatchDog
from mcdreforged.handler.server_handler_manager import ServerHandlerManager
from mcdreforged.info_reactor.info import Info
from mcdreforged.info_reactor.info_reactor_manager import InfoReactorManager
from mcdreforged.info_reactor.server_information import ServerInformation
from mcdreforged.mcdr_config import MCDReforgedConfig
from mcdreforged.mcdr_state import ServerState, MCDReforgedState, MCDReforgedFlag
from mcdreforged.minecraft.rcon.rcon_manager import RconManager
from mcdreforged.permission.permission_manager import PermissionManager
from mcdreforged.plugin.plugin_event import MCDRPluginEvents
from mcdreforged.plugin.plugin_manager import PluginManager
from mcdreforged.plugin.server_interface import ServerInterface
from mcdreforged.preference.preference_manager import PreferenceManager
from mcdreforged.translation.translation_manager import TranslationManager
from mcdreforged.utils import file_util
from mcdreforged.utils.exception import ServerStartError, IllegalStateError, DecodeError
from mcdreforged.utils.logger import DebugOption, MCDReforgedLogger, MCColorFormatControl
from mcdreforged.utils.types import MessageText


class MCDReforgedServer:
	process: Optional[Popen]

	def __init__(self, *, generate_default_only: bool = False, initialize_environment: bool = False):
		"""
		:param generate_default_only: If set to true, MCDR will only generate the default configuration and permission files
		"""
		self.mcdr_state = MCDReforgedState.INITIALIZING
		self.server_state = ServerState.STOPPED
		self.server_state_cv = Condition()
		self.server_information = ServerInformation()
		self.process: Optional[Popen] = None
		self.flags = MCDReforgedFlag.NONE
		self.starting_server_lock = Lock()  # to prevent multiple start_server() call
		self.stop_lock = Lock()  # to prevent multiple stop() call
		self.config_change_lock = Lock()

		# will be assigned in on_config_changed()
		self.encoding_method = None  # type: Optional[str]
		self.decoding_method = None  # type: Optional[str]

		# --- Constructing fields --- #
		self.logger = MCDReforgedLogger()
		self.config = MCDReforgedConfig(self.logger)
		self.permission_manager = PermissionManager(self)
		self.basic_server_interface = ServerInterface(self)
		self.task_executor = TaskExecutor(self)
		self.console_handler = ConsoleHandler(self)
		self.watch_dog = WatchDog(self)
		self.update_helper = UpdateHelper(self)
		self.translation_manager = TranslationManager(self.logger)
		self.rcon_manager = RconManager(self)
		self.server_handler_manager = ServerHandlerManager(self)
		self.reactor_manager = InfoReactorManager(self)
		self.command_manager = CommandManager(self)
		self.plugin_manager = PluginManager(self)
		self.preference_manager = PreferenceManager(self)

		self.__check_environment()

		# --- Input arguments "generate_default_only" processing --- #
		if generate_default_only:
			self.config.save_default()
			self.permission_manager.save_default()
			return

		# --- Initialize fields instance --- #
		self.translation_manager.load_translations()  # translations are used for logging, so load them first
		if initialize_environment:
			# Prepare config / permission files if they're missing
			if not self.config.file_presents():
				self.config.save_default()
				default_config = self.config.get_default_yaml()
				file_util.touch_directory(default_config['working_directory'])  # create server/ folder
			if not self.permission_manager.file_presents():
				self.permission_manager.save_default()

		# Check if there's any file missing
		# If there's any, MCDR environment might not be probably setup
		file_missing = False

		def load(kind: str, func: Callable[[], Any]) -> bool:
			nonlocal file_missing
			try:
				func()
			except FileNotFoundError:
				self.logger.error('{} is missing'.format(kind.title()))
				file_missing = True
			except YAMLError as e:
				self.logger.error('Failed to load {}: {}'.format(kind, type(e).__name__))
				for line in str(e).splitlines():
					self.logger.error(line)
				return False
			else:
				return True

		# load_config: config, language, handlers, plugin directories, reactors, handlers
		# load_permission_file: permission
		# config change will lead to creating plugin folders
		loading_success = \
			load('configuration', lambda: self.load_config(allowed_missing_file=False, log=not initialize_environment)) and \
			load('permission', lambda: self.permission_manager.load_permission_file(allowed_missing_file=False))
		if file_missing:
			self.__on_file_missing()
			return
		if not loading_success:
			return

		# MCDR environment has been set up, so continue creating default folders and loading stuffs
		self.logger.set_file(core_constant.LOGGING_FILE)  # will create logs/ folder
		self.plugin_manager.touch_directory()  # will create config/ folder

		# --- Done --- #
		self.set_mcdr_state(MCDReforgedState.INITIALIZED)

	def __del__(self):
		try:
			if self.process and self.process.poll() is None:
				self.__kill_server()
		except Exception:
			pass

	def __check_environment(self):
		"""
		Environment check at initialization. Warn and sleep if any of following conditions is met

		* mcdreforged package not found
		* current __file__ is not inside the mcdreforged package

		In dev environment, you can use setup.py to create `mcdreforged.egg-info/` so the package check can pass
		"""
		from_source_reason = None
		mcdr_pkg = core_constant.PACKAGE_NAME  # should be "mcdreforged"
		try:
			distributions: List[pkg_resources.Distribution] = pkg_resources.require(mcdr_pkg)
		except pkg_resources.ResolutionError:
			from_source_reason = '{} distribution is not found in python packages'.format(mcdr_pkg)
		else:
			for distribution in distributions:
				if distribution.project_name == mcdr_pkg:
					current_path = Path(__file__).absolute()
					distribution_path = Path(distribution.location).absolute()

					# distribution_path/mcdreforged/mcdr_server.py
					if not current_path.parent.parent.samefile(distribution_path):
						from_source_reason = 'current source path ({}) is not in {} distribution path ({})'.format(current_path, mcdr_pkg, distribution_path)
					break

		if from_source_reason is not None:
			self.logger.warning('Looks like you\'re launching MCDR from source, since {}'.format(from_source_reason))
			self.logger.warning('In this way, the plugin system might not work correctly, and the maintainability of MCDR will be very poor')
			self.logger.warning('In a production environment, you should install {} from PyPI, NOT from source codes'.format(mcdr_pkg))
			self.logger.warning('See document ({}) for more information'.format(core_constant.DOCUMENTATION_URL))
			self.logger.warning('MCDR will launch after 20 seconds...')
			time.sleep(20)

	def __on_file_missing(self):
		self.logger.info('Looks like MCDR is not initialized at current directory {}'.format(os.getcwd()))
		self.logger.info('Use command "{} init" to initialize MCDR first'.format(core_constant.CLI_COMMAND))
		self.logger.info('See document https://mcdreforged.readthedocs.io/en/latest/quick_start.html#start-up')

	# --------------------------
	#         Translate
	# --------------------------

	def get_language(self) -> str:
		return self.translation_manager.language

	def tr(self, translation_key: str, *args, language: Optional[str] = None, allow_failure=True, **kwargs) -> MessageText:
		"""
		Return a translated text corresponded to the translation key and format the text with given args
		If args contains RText element, then the result will be a RText, otherwise the result will be a regular str
		If the translation key is not recognized, the return value will be the translation key itself if allow_failure is True
		:param translation_key: The key of the translation
		:param args: The args to be formatted
		:param language: Specific language to be used in this translation, or the language that MCDR is using will be used
		:param allow_failure: If set to false, a KeyError will be risen if the translation key is not recognized
		:param kwargs: The kwargs to be formatted
		"""
		return self.translation_manager.translate(
			translation_key, args, kwargs,
			allow_failure=allow_failure,
			language=language,
			fallback_language=self.translation_manager.language,
			plugin_translations=self.plugin_manager.registry_storage.translations
		)

	# --------------------------
	#          Loaders
	# --------------------------

	def load_config(self, *, allowed_missing_file: bool = True, log: bool = True):
		has_missing = self.config.read_config(allowed_missing_file)
		# load the language before warning missing config to make sure translation is available
		self.on_config_changed(log=log)
		if log and has_missing:
			for line in self.tr('config.missing_config').splitlines():
				self.logger.warning(line)

	def on_config_changed(self, *, log: bool):
		with self.config_change_lock:
			MCColorFormatControl.console_color_disabled = self.config['disable_console_color']
			self.logger.set_debug_options(self.config['debug'])
			if log and self.config.is_debug_on():
				self.logger.info(self.tr('mcdr_server.on_config_changed.debug_mode_on'))

			self.translation_manager.set_language(self.config['language'])
			if log:
				self.logger.info(self.tr('mcdr_server.on_config_changed.language_set', self.config['language']))

			self.encoding_method = self.config['encoding'] or locale.getpreferredencoding()
			self.decoding_method = self.config['decoding'] or locale.getpreferredencoding()
			if log:
				self.logger.info(self.tr('mcdr_server.on_config_changed.encoding_decoding_set', self.encoding_method, self.decoding_method))

			self.plugin_manager.set_plugin_directories(self.config['plugin_directories'])
			if log:
				self.logger.info(self.tr('mcdr_server.on_config_changed.plugin_directories_set', self.encoding_method, self.decoding_method))
				for directory in self.plugin_manager.plugin_directories:
					self.logger.info('- {}'.format(directory))

			self.reactor_manager.register_reactors(self.config['custom_info_reactors'])

			self.server_handler_manager.register_handlers(self.config['custom_handlers'])
			self.server_handler_manager.set_handler(self.config['handler'])
			if log:
				self.logger.info(self.tr('mcdr_server.on_config_changed.handler_set', self.config['handler']))

			self.connect_rcon()

	def load_plugins(self):
		future = self.plugin_manager.refresh_all_plugins()
		self.logger.info(future.get().to_rtext(self, show_path=True))

	def on_plugin_registry_changed(self):
		self.command_manager.clear_command()
		self.plugin_manager.registry_storage.export_commands(self.command_manager.register_command)

	# ---------------------------
	#      General Setters
	# ---------------------------
	# for field read-only access, simply use directly reference
	# but for field writing operation, use setters

	def set_task_executor(self, new_task_executor: TaskExecutor):
		self.task_executor = new_task_executor

	# ---------------------------
	#   State Getters / Setters
	# ---------------------------

	def is_server_running(self):
		return self.server_state.in_state(ServerState.RUNNING, ServerState.STOPPING)

	# Flags

	def is_server_startup(self):
		return MCDReforgedFlag.SERVER_STARTUP in self.flags

	def is_server_rcon_ready(self):
		return MCDReforgedFlag.SERVER_RCON_READY in self.flags

	def is_interrupt(self):
		return MCDReforgedFlag.INTERRUPT in self.flags

	def is_mcdr_exit(self):
		return self.mcdr_in_state(MCDReforgedState.STOPPED)

	def is_mcdr_about_to_exit(self):
		return self.mcdr_in_state(MCDReforgedState.PRE_STOPPED, MCDReforgedState.STOPPED)

	def should_exit_after_stop(self):
		return MCDReforgedFlag.EXIT_AFTER_STOP in self.flags

	def add_flag(self, flag: MCDReforgedFlag):
		self.flags |= flag
		self.logger.debug('Added MCDReforgedFlag {}'.format(flag), option=DebugOption.MCDR)

	def remove_flag(self, flag: MCDReforgedFlag):
		self.flags &= ~flag
		self.logger.debug('Removed MCDReforgedFlag {}'.format(flag), option=DebugOption.MCDR)

	# State

	def server_in_state(self, *states: ServerState) -> bool:
		return self.server_state.in_state(*states)

	def mcdr_in_state(self, *states: MCDReforgedState) -> bool:
		return self.mcdr_state.in_state(*states)

	def is_initialized(self):
		return self.mcdr_in_state(MCDReforgedState.INITIALIZED)

	def set_server_state(self, state):
		self.server_state = state
		self.logger.debug('Server state has set to "{}"'.format(state), option=DebugOption.MCDR)
		with self.server_state_cv:
			self.server_state_cv.notify_all()

	def set_mcdr_state(self, state):
		self.mcdr_state = state
		self.logger.debug('MCDR state has set to "{}"'.format(state), option=DebugOption.MCDR)

	def should_keep_looping(self):
		"""
		A criterion for sub threads to determine if it should keep looping
		:rtype: bool
		"""
		if self.server_in_state(ServerState.STOPPED):
			if self.is_interrupt():  # if interrupted and stopped
				return False
			if self.should_exit_after_stop():  # natural server stop, or server_interface.exit() by plugin
				return False
			return True
		return not self.is_mcdr_exit()

	# --------------------------
	#      Server Controls
	# --------------------------

	def start_server(self):
		"""
		try to start the server process
		return True if the server process has started successfully
		return False if the server is not able to start

		:return: a bool as above
		:rtype: bool
		"""
		with self.starting_server_lock:
			if self.is_interrupt():
				self.logger.warning(self.tr('mcdr_server.start_server.already_interrupted'))
				return False
			if self.is_server_running():
				self.logger.warning(self.tr('mcdr_server.start_server.start_twice'))
				return False
			if self.is_mcdr_about_to_exit():
				self.logger.warning(self.tr('mcdr_server.start_server.about_to_exit'))
				return False
			cwd = self.config['working_directory']
			if not os.path.isdir(cwd):
				self.logger.error(self.tr('mcdr_server.start_server.cwd_not_existed', cwd))
				return False
			try:
				start_command = self.config['start_command']
				self.logger.info(self.tr('mcdr_server.start_server.starting', start_command))
				self.process = Popen(start_command, cwd=self.config['working_directory'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
			except Exception:
				self.logger.exception(self.tr('mcdr_server.start_server.start_fail'))
				return False
			else:
				self.__on_server_start()
				return True

	def __kill_server(self):
		"""
		Kill the server process group
		"""
		if self.process and self.process.poll() is None:
			self.logger.info(self.tr('mcdr_server.kill_server.killing'))
			try:
				root = psutil.Process(self.process.pid)
				processes = [root]
				processes.extend(root.children(recursive=True))
				for proc in reversed(processes):  # child first, parent last
					try:
						proc_pid, proc_name = proc.pid, proc.name()  # in case we cannot get them after the process dies
						proc.kill()
						self.logger.info(self.tr('mcdr_server.kill_server.process_killed', proc_name, proc_pid))
					except psutil.NoSuchProcess:
						pass
			except psutil.NoSuchProcess:
				pass
			self.process.poll()
		else:
			self.logger.warning('Try to kill the server when the server process has already been terminated')

	def interrupt(self) -> bool:
		"""
		Interrupt MCDR
		The first call will softly stop the server and the later calls will kill the server
		Return if it's the first try
		"""
		first_interrupt = not self.is_interrupt()
		self.logger.info(self.tr('mcdr_server.interrupt.{}'.format('soft' if first_interrupt else 'hard')))
		if self.is_server_running():
			self.stop(forced=not first_interrupt)
		self.add_flag(MCDReforgedFlag.INTERRUPT)
		return first_interrupt

	def stop(self, forced: bool = False) -> bool:
		"""
		Stop the server

		:param forced: an optional bool. If it's False (default) MCDR will stop the server by sending the STOP_COMMAND from the
		current handler. If it's True MCDR will just kill the server process group
		"""
		with self.stop_lock:
			if not self.is_server_running():
				self.logger.warning(self.tr('mcdr_server.stop.stop_when_stopped'))
				return False
			self.set_server_state(ServerState.STOPPING)
			if not forced:
				try:
					self.send(self.server_handler_manager.get_current_handler().get_stop_command())
				except Exception:
					self.logger.error(self.tr('mcdr_server.stop.stop_fail'))
					forced = True
			if forced:
				self.__kill_server()
			return True

	# --------------------------
	#      Server Logics
	# --------------------------

	def __on_server_start(self):
		self.set_server_state(ServerState.RUNNING)
		self.add_flag(MCDReforgedFlag.EXIT_AFTER_STOP)  # Set after server state is set to RUNNING, or MCDR might have a chance to exit if the server is started by other thread
		self.logger.info(self.tr('mcdr_server.start_server.pid_info', self.process.pid))
		self.reactor_manager.on_server_start()
		self.plugin_manager.dispatch_event(MCDRPluginEvents.SERVER_START, ())

	def __on_server_stop(self):
		return_code = self.process.poll()
		self.logger.info(self.tr('mcdr_server.on_server_stop.show_return_code', return_code))
		try:
			self.process.stdin.close()
		except Exception as e:
			self.logger.warning('Error when closing stdin: {}'.format(e))
		try:
			self.process.stdout.close()
		except Exception as e:
			self.logger.warning('Error when closing stdout: {}'.format(e))
		self.process = None
		self.set_server_state(ServerState.STOPPED)
		self.remove_flag(MCDReforgedFlag.SERVER_STARTUP | MCDReforgedFlag.SERVER_RCON_READY)  # removes this two
		self.reactor_manager.on_server_stop()
		self.plugin_manager.dispatch_event(MCDRPluginEvents.SERVER_STOP, (return_code,), block=True)

		if self.is_interrupt():
			self.logger.info(self.tr('mcdr_server.on_server_stop.user_interrupted'))
		else:
			self.logger.info(self.tr('mcdr_server.on_server_stop.server_stop'))

	def send(self, text, ending='\n', encoding=None):
		"""
		Send a text to server's stdin if the server is running

		:param text: A str or a bytes you want to send. if text is a str then it will attach the ending parameter to its
		back
		:param str ending: The suffix of a command with a default value \n
		:param str encoding: The encoding method for the text. If it's not given used the method in config
		"""
		if encoding is None:
			encoding = self.encoding_method
		if isinstance(text, str):
			encoded_text = (text + ending).encode(encoding)
		elif isinstance(text, bytes):
			encoded_text = text
		else:
			raise TypeError()
		if self.is_server_running():
			self.process.stdin.write(encoded_text)
			self.process.stdin.flush()
		else:
			self.logger.warning(self.tr('mcdr_server.send.send_when_stopped'))
			self.logger.warning(self.tr('mcdr_server.send.send_when_stopped.text', text if len(text) <= 32 else text[:32] + '...'))

	def __receive(self) -> Optional[str]:
		"""
		Try to receive a str from server's stdout. This will block the current thread

		If server has stopped it will wait up to 60s for the server process to exit, then return None
		"""
		try:
			line_buf: bytes = next(iter(self.process.stdout))
		except StopIteration:  # server process has stopped
			for i in range(core_constant.WAIT_TIME_AFTER_SERVER_STDOUT_END_SEC):
				try:
					self.process.wait(1)
				except TimeoutExpired:
					self.logger.info(self.tr('mcdr_server.receive.wait_stop'))
				else:
					break
			else:
				self.logger.warning('The server is still not stopped after {}s after its stdout was closed, killing'.format(core_constant.WAIT_TIME_AFTER_SERVER_STDOUT_END_SEC))
				self.__kill_server()
			self.process.wait()
			return None
		else:
			try:
				line_text: str = line_buf.decode(self.decoding_method)
			except Exception as e:
				self.logger.error(self.tr('mcdr_server.receive.decode_fail', line_buf, e))
				raise DecodeError()
			return line_text.strip('\n\r')

	def __tick(self):
		"""
		ticking MCDR:
		try to receive a new line from server's stdout and parse / display / process the text
		"""
		try:
			text = self.__receive()
		except DecodeError:
			return

		if text is None:  # server stops
			self.__on_server_stop()
			return

		try:
			text = self.server_handler_manager.get_current_handler().pre_parse_server_stdout(text)
		except Exception:
			self.logger.warning(self.tr('mcdr_server.tick.pre_parse_fail'))

		parsed_result: Info
		try:
			parsed_result = self.server_handler_manager.get_current_handler().parse_server_stdout(text)
		except Exception:
			if self.logger.should_log_debug(option=DebugOption.HANDLER):  # traceback.format_exc() is costly
				self.logger.debug('Fail to parse text "{}" from stdout of the server, using raw handler'.format(text), no_check=True)
				for line in traceback.format_exc().splitlines():
					self.logger.debug('    {}'.format(line), no_check=True)
			parsed_result = self.server_handler_manager.get_basic_handler().parse_server_stdout(text)
		else:
			if self.logger.should_log_debug(option=DebugOption.HANDLER):
				self.logger.debug('Parsed text from server stdout:', no_check=True)
				for line in parsed_result.debug_format_text().splitlines():
					self.logger.debug('    {}'.format(line), no_check=True)
		self.server_handler_manager.detect_text(text)
		self.reactor_manager.put_info(parsed_result)

	def __on_mcdr_start(self):
		self.__register_signal_handler()
		self.watch_dog.start()
		self.task_executor.start()
		self.preference_manager.load_preferences()
		self.plugin_manager.register_permanent_plugins()
		self.task_executor.execute_on_thread(self.load_plugins, block=True)
		self.plugin_manager.dispatch_event(MCDRPluginEvents.MCDR_START, ())
		if not self.config['disable_console_thread']:
			self.console_handler.start()
		else:
			self.logger.info(self.tr('mcdr_server.on_mcdr_start.console_disabled'))
		if not self.start_server():
			raise ServerStartError()
		self.update_helper.start()
		if self.config['handler_detection']:
			self.server_handler_manager.start_handler_detection()
		self.set_mcdr_state(MCDReforgedState.RUNNING)

	def __register_signal_handler(self):
		def callback(sig: int, frame):
			try:
				signal_name = signal.Signals(sig).name
			except ValueError:
				signal_name = 'unknown'
			self.logger.warning('Received signal {} ({}), interrupting MCDR'.format(signal_name, sig))
			self.interrupt()

		import signal
		signal.signal(signal.SIGINT, callback)   # ctrl + c
		signal.signal(signal.SIGTERM, callback)  # graceful termination

	def __on_mcdr_stop(self):
		try:
			self.set_mcdr_state(MCDReforgedState.PRE_STOPPED)

			self.logger.info(self.tr('mcdr_server.on_mcdr_stop.info'))

			self.plugin_manager.dispatch_event(MCDRPluginEvents.PLUGIN_UNLOADED, ())
			self.task_executor.wait_till_finish_all_task()
			with self.watch_dog.pausing():  # it's ok for plugins to take some time
				self.plugin_manager.dispatch_event(MCDRPluginEvents.MCDR_STOP, (), block=True)

			self.console_handler.stop()
			self.logger.info(self.tr('mcdr_server.on_mcdr_stop.bye'))
		except KeyboardInterrupt:  # I don't know why there sometimes will be a KeyboardInterrupt if MCDR is stopped by ctrl-c
			pass
		except Exception:
			self.logger.exception(self.tr('mcdr_server.on_mcdr_stop.stop_error'))
		finally:
			self.set_mcdr_state(MCDReforgedState.STOPPED)

	def run_mcdr(self):
		"""
		The entry method to start MCDR
		Try to start the server. if succeeded the console thread will start and MCDR will start ticking

		:raise: IllegalStateError if MCDR is in wrong state
		:raise: ServerStartError if the server is already running or start_server has been called by other
		"""
		if not self.mcdr_in_state(MCDReforgedState.INITIALIZED):
			if self.mcdr_in_state(MCDReforgedState.INITIALIZING):
				raise IllegalStateError('This instance is not fully initialized')
			else:
				raise IllegalStateError('MCDR can only start once')
		self.__main_loop()
		return self.process

	def __main_loop(self):
		"""
		The main loop of MCDR
		"""
		self.__on_mcdr_start()
		while self.should_keep_looping():
			try:
				if self.is_server_running():
					self.__tick()
				else:
					with self.server_state_cv:
						self.server_state_cv.wait(0.01)
			except KeyboardInterrupt:
				self.interrupt()
			except Exception:
				if self.is_interrupt():
					break
				else:
					self.logger.critical(self.tr('mcdr_server.run.error'), exc_info=True)
		self.__on_mcdr_stop()

	def connect_rcon(self):
		self.rcon_manager.disconnect()
		if self.config['rcon']['enable'] and self.is_server_rcon_ready():
			self.rcon_manager.connect(self.config['rcon']['address'], self.config['rcon']['port'], self.config['rcon']['password'])
