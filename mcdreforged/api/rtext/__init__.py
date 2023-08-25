# Link to mcdreforged.rtext
# The advance text component class for Minecraft
from mcdreforged.minecraft.rtext.style import RColor, RStyle, RAction, RColorClassic, RColorRGB, RStyleClassic
from mcdreforged.minecraft.rtext.text import RTextTranslation, RTextList, RTextBase, RText
from mcdreforged.translation.translation_text import RTextMCDRTranslation

__all__ = [
	'RColor', 'RColorRGB', 'RColorClassic',
	'RStyle', 'RStyleClassic',
	'RAction',
	'RTextBase', 'RText', 'RTextTranslation', 'RTextList',
	'RTextMCDRTranslation'
]
