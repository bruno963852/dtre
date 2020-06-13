import logging
import os
import sys
import traceback
from typing import Dict

from discord import File, User
from discord.ext import commands
from discord.ext.commands import CheckFailure, Context

from src.bot.character_commands import CharacterCommands
from src.bot.dice_roll_commands import DiceRollCommands
from src.bot.discord_logging_handler import DiscordLoggingHandler
from src.bot.misc_commands import MiscCommands
from src.bot.scenario_commands import ScenarioCommands
from src.image.exceptions import CharacterNotFoundException, InvalidMovementException, FrameWithoutAlphaException
from src.scenario import Scenario

TOKEN = os.environ["DISCORD_TOKEN"]
USER_ID = int(os.environ["USER_ID"])

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

    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format="-------------------------------\n*%(asctime)s* **[%(levelname)s]** \n**Message:** %(message)s",
        handlers=[
            logging.FileHandler('../debug.log'),
            logging.StreamHandler(sys.stdout),
            DiscordLoggingHandler(bot)
        ]
    )

    logging.info(f'Logged in as "{bot.user.name}" / {bot.user.id}')


@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    ctx   : Context
    error : Exception"""

    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound,)
    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        pass
    
    elif isinstance(error, commands.UserInputError):
        await ctx.send(f'There was an **error** in the command arguments...')

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled...')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages...')
        except:
            pass

    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':
            return await ctx.send('I could not find that member. Please try again.')

    await ctx.send('I rolled a **Critical Failure** executinng that command...')

    logging.error('Ignoring exception in command {}:'.format(ctx.command))
    logging.error('Stack info', stack_info=True)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def run():
    bot.run(TOKEN)
