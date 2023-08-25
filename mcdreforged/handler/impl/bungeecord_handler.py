import re
from typing import Optional

import parse

from mcdreforged.handler.abstract_server_handler import AbstractServerHandler
from mcdreforged.info_reactor.info import Info
from mcdreforged.info_reactor.server_information import ServerInformation
from mcdreforged.utils.types import MessageText


class BungeecordHandler(AbstractServerHandler):
	"""
	A handler for `Bungeecord <https://github.com/SpigotMC/BungeeCord>`__ servers
	"""
	def get_stop_command(self) -> str:
		return 'end'

	def get_send_message_command(self, target: str, message: MessageText, server_information: ServerInformation) -> Optional[str]:
		return None

	def get_broadcast_message_command(self, message: MessageText, server_information: ServerInformation) -> Optional[str]:
		from mcdreforged.handler.impl import VanillaHandler
		return 'alertraw {}'.format(VanillaHandler.format_message(message))

	@classmethod
	def get_content_parsing_formatter(cls):
		# 09:00:02 [信息] Listening on /0.0.0.0:25565
		# 09:00:01 [信息] [Steve] -> UpstreamBridge has disconnected
		return '{hour:d}:{min:d}:{sec:d} [{logging}] {content}'

	__prompt_text_regex = re.compile(r'>*\r')

	def pre_parse_server_stdout(self, text):
		text = super().pre_parse_server_stdout(text)
		match = self.__prompt_text_regex.match(text)
		if match is not None:
			text = text.replace(match.group(), '', 1)
		return text

	__player_joined_parser = parse.Parser('[{name},/{ip}] <-> InitialHandler has connected')
	__player_left_parser = parse.Parser('[{name}] -> UpstreamBridge has disconnected')
	__server_address_parser = parse.Parser('Listening on /{}:{:d}')
	__server_startup_done_regex = re.compile(r'Listening on /[0-9.]+:[0-9]+')
	__server_stopping_regex = re.compile(r'Closing listener \[id: .+, L:[\d:/]+]')

	def parse_player_joined(self, info: Info) -> Optional[str]:
		# [Steve,/127.0.0.1:3631] <-> InitialHandler has connected
		if not info.is_user:
			parsed = self.__player_joined_parser.parse(info.content)
			if parsed is not None:
				return parsed['name']
		return None

	def parse_player_left(self, info):
		# [Steve] -> UpstreamBridge has disconnected
		if not info.is_user:
			parsed = self.__player_left_parser.parse(info.content)
			if parsed is not None:
				return parsed['name']
		return None

	def parse_server_version(self, info: Info):
		return None

	def parse_server_address(self, info: Info):
		# Listening on /0.0.0.0:25577
		if not info.is_user:
			parsed = self.__server_address_parser.parse(info.content)
			if parsed is not None:
				return parsed[0], parsed[1]
		return None

	def test_server_startup_done(self, info: Info) -> bool:
		# Listening on /0.0.0.0:25577
		return not info.is_user and self.__server_startup_done_regex.fullmatch(info.content) is not None

	def test_rcon_started(self, info: Info) -> bool:
		return self.test_server_startup_done(info)

	def test_server_stopping(self, info: Info) -> bool:
		# Closing listener [id: 0x3acae0b0, L:/0:0:0:0:0:0:0:0:25565]
		return not info.is_user and self.__server_stopping_regex.fullmatch(info.content) is not None
