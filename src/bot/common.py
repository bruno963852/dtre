from typing import Dict

from discord import File
from discord.ext.commands import Context

from src.char import Character


async def post_scenario(ctx: Context, image: File, chars: Dict[str, Character]):
    message = ''
    if len(chars) > 0:
        message += "```md\n"
        for index, char in enumerate(chars):
            message += f'{index}. {char}\n'
        message += "```"
    await ctx.send(content=message, file=image)