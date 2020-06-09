import os
import traceback
from typing import Dict

from discord import File
from discord.ext import commands
from discord.ext.commands import CheckFailure, Context

from src.bot.character_commands import CharacterCommands
from src.bot.dice_roll_commands import DiceRollCommands
from src.bot.misc_commands import MiscCommands
from src.bot.scenario_commands import ScenarioCommands
from src.image.exceptions import CharacterNotFoundException, InvalidMovementException, FrameWithoutAlphaException
from src.scenario import Scenario

TOKEN = os.environ["DISCORD_TOKEN"]

DESCRIPTION = '''DTRE is a tabletop rpg engine to be used in discord. If you're tired of complicated tools, 
but want some more functionality and want a simple streamlined roleplaying experience directly on discord, 
with no external apps, and that can be easily playable on mobile search no further. '''

COMMAND_PREFIXES = ('?drpg.', '!dprg.', '?r.', '!r.')

DM_CHANNEL_NAME = 'DTRE_DM'

bot = commands.Bot(command_prefix=COMMAND_PREFIXES, description=DESCRIPTION)


@bot.event
async def on_ready():
    bot.add_cog(MiscCommands(bot))
    bot.add_cog(ScenarioCommands(bot))
    bot.add_cog(CharacterCommands(bot))
    bot.add_cog(DiceRollCommands(bot))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.check
async def check_permission(ctx: commands.Context):
    if not ctx.channel.permissions_for(ctx.me).manage_messages:
        await ctx.send('O bot precisa da permissão de "Gerenciar Mensagens" para apagar as mensagens do canal da mesa')
        return False
    elif not ctx.channel.permissions_for(ctx.me).manage_channels:
        await ctx.send('O bot precisa da permissão de "Gerenciar Canais" para criar o canal da mesa')
        return False
    # await ctx.message.delete()
    return True


# @bot.event
# async def on_command_error(ctx: commands.Context, error: commands.CommandError):
#     print(error)
#     if error is CheckFailure:
#         await ctx.send("Erro, o bot não tem as permissões necessárias...")
#     else:
#         await ctx.send("Houve um erro inesperado...")


def run():
    bot.run(TOKEN)
