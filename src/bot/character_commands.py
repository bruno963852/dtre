import json
import traceback

from discord import File
from discord.ext.commands import Cog, command, Context

from src.bot import dontpad
from src.bot.dontpad import DTRE_URL
from src.char import Character
from src.image.exceptions import CharacterNotFoundInScenarioException, InvalidMovementException, \
    CharacterNotFoundInDatabaseException
from src.image.player_token import Token
from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


def _get_char_data(guild_id: str, channel_id: str):
    url = f'{DTRE_URL}/{guild_id}/{channel_id}/chars'
    data = dontpad.read(url)
    if data is None:
        data = '{}'
    return json.loads(data)


def _save_char_data(guild_id: str, channel_id: str, char_data: dict):
    url = f'{DTRE_URL}/{guild_id}/{channel_id}/chars'
    dontpad.write(url, json.dumps(char_data))


class CharacterCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _add_character(guild_id, channel_id, name, url, position_x, position_y, size_x, size_y) -> File:
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        char = Character(
            name,
            Token(
                name,
                (position_x, position_y),
                url,
                scenario.map.square_size,
                guild_id,
                channel_id,
                (size_x, size_y)
            )
        )
        scenario.add_character(char)
        return File(scenario.get_image(), filename='play_mat.png')

    @staticmethod
    def _remove_character(guild_id, channel_id, name) -> File:
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        scenario.remove_character(name)
        return File(scenario.get_image(), filename='play_mat.png')

    @staticmethod
    def _move_character(guild_id, channel_id, name, movement):
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        scenario.move_character(name, movement)
        return File(scenario.get_image(True), filename='play_mat.png')

    @staticmethod
    def _save_character(guild_id, channel_id, name):
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        try:
            char = scenario.characters[name]  # type: Character
            char_data = _get_char_data(guild_id, channel_id)
            char_data[char.name] = char.dict
            _save_char_data(guild_id, channel_id, char_data)
        except KeyError:
            raise CharacterNotFoundInScenarioException

    @staticmethod
    def _load_character(guild_id, channel_id, name):
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        try:
            char_data = _get_char_data(guild_id, channel_id)
            char_dict = char_data[name]
            char = Character.from_dict(char_dict, guild_id, channel_id, scenario.map.square_size)
            scenario.add_character(char)
            return File(scenario.get_image(), filename='play_mat.png')
        except KeyError:
            raise CharacterNotFoundInDatabaseException

    @command(aliases=['ac', 'addcharacter', 'addchar', 'add_char', 'Ac'],
             help="""Adds a character to the scenario
                params:
                name: Name of the character
                position_x: position for the character token in the map on the x axis (from left)
                position_y: position for the character token in the map on the y axis (from top)
                url: url of the image to be used as token (The image will be resized and cropped to a circle and put in 
                a frame)
                size_x: the size in map squares of the token in the x axis (not supported yet, omit this parameter)
                size_y: the size in map squares of the token in the y axis (not supported yet, omit this parameter)
                
                Examples:
                ?r.addchar valkor 2 2 https://i.pinimg.com/originals/96/96/c0/9696c0a9d2740224e6d99ffd14af48ef.jpg
                response: the map with the added token
                """,
             )
    async def add_character(self, ctx: Context, name: str, position_x: int = -1, position_y: int = -1, url: str = '',
                            size_x: int = 1, size_y: int = 1):
        """
        Adds a character to the scenario
        @param ctx: the context passed by the API
        @param name: Name of the character
        @param position_x: position for the character token in the map on the x axis (from left)
        @param position_y: position for the character token in the map on the y axis (from top)
        @param url: url of the image to be used as token (The image will be resized and cropped to a circle and put in
        a frame)
        @param size_x: the size in map squares of the token in the x axis
        @param size_y: the size in map squares of the token in the y axis
        @return: None
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)

        await ctx.send("Processing...")

        if (position_x, position_y) == (-1, -1):
            image = await self.bot.loop.run_in_executor(None, self._load_character, guild_id, channel_id, name)
            await ctx.send(file=image)
            return

        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url

        image = await self.bot.loop.run_in_executor(None, self._add_character, guild_id, channel_id, name, url,
                                                    position_x, position_y, size_x, size_y)
        await ctx.send(file=image)

    @command(aliases=['rc', 'removecharacter', 'removechar', 'remove_char', 'Rc'],
             help="""Removes a character from the scenario
                params:
                ctx: Context passed by the API
                name: the name of the character to be removed
                
                Examples:
                ?r.removechar valkor
                response: the map with the removed token
                """,
             )
    async def remove_character(self, ctx: Context, name: str):
        """
        Removes a character from the scenario
        @param name: the name of the character to be removed
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        image = await self.bot.loop.run_in_executor(None, self._remove_character, guild_id, channel_id, name)
        await ctx.send(file=image)

    @command(aliases=['m', 'mc', 'move_char', 'movecharacter', 'move', 'M'],
             help="""Moves a character
                The movement is defined by directions separated by spaces,
                the directions can be the orthogonal (u = up, l = left, d = down, ur = righ) or
                any combination of two orthogonal direction to for a diagonal (ex: ul for up-left)
                params:
                name: the name of the character to be moved
                movement: the movement of the character as described in the command help
                
                Examples:
                ?r.move valkor l ul l u
                ?r.move goblin2 rd rd rd r
                response: the map with the moved token
                """,
             )
    async def move_character(self, ctx: Context, name: str, *, movement: str):
        """
        Moves a character according to the movement indicated by the command
        @param ctx: Context passed by the API
        @param name: the name of the character to be moved
        @param movement: the movement of the character as described in the command description
        """

        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        await ctx.send("Processing...")
        image = await self.bot.loop.run_in_executor(None, self._move_character, guild_id, channel_id, name, movement)
        await ctx.send(file=image)

    @command(aliases=['sc', 'savecharacter', 'savechar', 'save_char', 'Sc'],
             help="""Saves a character in the permanent database
                    params:
                    name: the name of the character to be sved

                    Examples:
                    ?r.savechar valkor
                    response: confirmation if the char has been saved
                    """,
             )
    async def save_character(self, ctx: Context, name: str):
        """
        Removes a character from the scenario
        @param ctx: Context passed by the API
        @param name: the name of the character to be removed
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        await self.bot.loop.run_in_executor(None, self._save_character, guild_id, channel_id, name)
        await ctx.send(f'Character **{name}** saved successfully in the database!')
