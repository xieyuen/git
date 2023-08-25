from mcdreforged.handler.impl.abstract_minecraft_handler import AbstractMinecraftHandler


class VanillaHandler(AbstractMinecraftHandler):
	"""
	A handler for vanilla Minecraft servers
	"""
	@classmethod
	def get_content_parsing_formatter(cls):
		return '[{hour:d}:{min:d}:{sec:d}] [{thread}/{logging}]: {content}'
