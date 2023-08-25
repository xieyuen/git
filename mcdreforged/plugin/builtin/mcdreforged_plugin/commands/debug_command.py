import json
import threading
import traceback
from typing import List, Optional, Set, Dict

from mcdreforged.command.builder.nodes.arguments import QuotableText
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource
from mcdreforged.plugin.builtin.mcdreforged_plugin.commands.sub_command import SubCommand
from mcdreforged.plugin.plugin_registry import PluginCommandHolder
from mcdreforged.utils.types import TranslationStorage


def thread_dump(*, target_thread: Optional[str] = None) -> List[str]:
	# noinspection PyProtectedMember
	from sys import _current_frames
	lines = []
	stack_map = _current_frames().copy()
	for thread in threading.enumerate():
		thread_id, thread_name = thread.ident, thread.name
		if target_thread is not None and thread_name != target_thread:
			continue
		if thread_id in stack_map:
			lines.append("Thread {} (id {})".format(thread_name, thread_id))
			for filename, lineno, func_name, line in traceback.extract_stack(stack_map[thread_id]):
				lines.append('  File "{}", line {}, in {}'.format(filename, lineno, func_name))
				if line:
					lines.append('    {}'.format(line.strip()))
	return lines


def json_wrap(obj) -> str:
	return json.dumps(obj, indent=4, ensure_ascii=False)


class DebugCommand(SubCommand):
	def get_command_node(self) -> Literal:
		def translation_dump_suggest() -> Set[str]:
			result = {'.'}
			for k in self.translations.keys():
				segs = k.split('.')
				for i in range(len(segs)):
					result.add('.'.join(segs[: i + 1]))
			return result

		return (
			self.owner_command_root('debug').
			runs(lambda src: src.reply(self.get_help_message(src, 'mcdr_command.help_message.debug'))).
			then(
				Literal('thread_dump').
				runs(lambda src: self.show_thread_dump(src, None)).
				then(
					Literal('#all').
					runs(lambda src: self.show_thread_dump(src, None))
				).
				then(
					QuotableText('thread_name').
					suggests(lambda: map(lambda t: t.name, threading.enumerate())).
					runs(lambda src, ctx: self.show_thread_dump(src, ctx['thread_name']))
				)
			).
			then(
				Literal('translation').
				then(
					Literal('get').
					then(
						QuotableText('translation_key').
						suggests(lambda: self.translations.keys()).
						runs(lambda src, ctx: self.show_translation_entry(src, ctx['translation_key']))
					)
				).
				then(
					Literal('dump').
					then(
						QuotableText('json_path').
						suggests(translation_dump_suggest).
						runs(lambda src, ctx: self.show_translation_dump(src, ctx['json_path']))
					)
				)
			).
			then(
				Literal('command_dump').
				then(
					Literal('all').
					runs(lambda src: self.show_command_tree(src, show_all=True))
				).
				then(
					Literal('plugin').
					then(
						QuotableText('plugin_id').
						suggests(lambda: map(lambda plg: plg.get_id(), self.mcdr_server.plugin_manager.get_all_plugins())).
						runs(lambda src, ctx: self.show_command_tree(src, plugin_id=ctx['plugin_id']))
					)
				).
				then(
					Literal('node').
					then(
						QuotableText('literal_name').
						suggests(lambda: self.command_roots.keys()).
						runs(lambda src, ctx: self.show_command_tree(src, literal_name=ctx['literal_name']))
					)
				)
			)
		)

	@property
	def translations(self) -> TranslationStorage:
		return {**self.mcdr_server.plugin_manager.registry_storage.translations, **self.mcdr_server.translation_manager.translations}

	@property
	def command_roots(self) -> Dict[str, List[PluginCommandHolder]]:
		return self.mcdr_server.command_manager.root_nodes.copy()

	def show_thread_dump(self, source: CommandSource, target_thread: Optional[str]):
		for line in thread_dump(target_thread=target_thread):
			source.reply(line)

	def show_translation_entry(self, source: CommandSource, translation_key: str):
		entry = self.translations.get(translation_key.strip('.'))
		source.reply(json_wrap(entry))

	def show_translation_dump(self, source: CommandSource, json_path: str):
		prefix_segments = list(filter(None, json_path.strip('.').split('.')))
		ret = {}
		for key, value in self.translations.items():
			key_segments = key.split('.')
			if key_segments[:len(prefix_segments)] == prefix_segments:
				ret[key] = value
		source.reply(json_wrap(ret))

	def show_command_tree(self, source: CommandSource, *, show_all: bool = False, plugin_id: Optional[str] = None, literal_name: Optional[str] = None):
		roots: Dict[str, List[PluginCommandHolder]] = self.command_roots
		for literal, holders in roots.items():
			if not show_all and (literal_name is not None and literal != literal_name):
				continue
			for holder in holders:
				if show_all or (plugin_id is None or holder.plugin.get_id() == plugin_id):
					holder.node.print_tree(source.reply)
