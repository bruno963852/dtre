import json
import math
import traceback
from typing import Tuple

from discord import File
from discord.ext.commands import Cog, command, Context

from src.bot import dontpad
from src.bot.common import post_scenario
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
    def _add_character(guild_id, channel_id, name, url, position_x, position_y, size_x, size_y) -> Tuple[File, dict]:
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
        return File(scenario.get_image(), filename='play_mat.png'), scenario.characters

    @staticmethod
    def _remove_character(guild_id, channel_id, name) -> Tuple[File, dict]:
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        scenario.remove_character(name)
        return File(scenario.get_image(), filename='play_mat.png'), scenario.characters

    @staticmethod
    def _move_character(guild_id, channel_id, name, movement) -> Tuple[File, dict]:
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        scenario.move_character(name, movement)
        return File(scenario.get_image(True), filename='play_mat.png'), scenario.characters

    @staticmethod
    def _save_character(guild_id, channel_id, name, url, size):
        if url != '':
            char = Character(name, Token(name, (1, 1), url, 45, guild_id, channel_id, size))
        else:
            try:
                scenario = Scenarios.get_scenario(guild_id, channel_id)
                char = scenario.characters[name]  # type: Character
            except KeyError:
                raise CharacterNotFoundInScenarioException
        char_data = _get_char_data(guild_id, channel_id)
        char_data[char.name] = char.dict
        _save_char_data(guild_id, channel_id, char_data)

    @staticmethod
    def _load_character(guild_id, channel_id, name, position) -> Tuple[File, dict]:
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        alias = None
        if '/' in name:
            name, alias = name.split('/')
        try:
            char_data = _get_char_data(guild_id, channel_id)
            char_dict = char_data[name]
            char = Character.from_dict(char_dict, guild_id, channel_id, scenario.map.square_size)
            char.token.position = position
            if alias:
                char.name = alias
            scenario.add_character(char)
            return File(scenario.get_image(), filename='play_mat.png'), scenario.characters
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
    async def add_character(self, ctx: Context, name: str, position_x: int, position_y: int, url: str = '',
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

        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
            else:
                image, chars = await self.bot.loop.run_in_executor(None, self._load_character, guild_id, channel_id,
                                                                   name, (position_x, position_y))
                await post_scenario(ctx, image, chars)
                return

        image, chars = await self.bot.loop.run_in_executor(None, self._add_character, guild_id, channel_id, name, url,
                                                           position_x, position_y, size_x, size_y)
        await post_scenario(ctx, image, chars)

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
        image, chars = await self.bot.loop.run_in_executor(None, self._remove_character, guild_id, channel_id, name)
        await post_scenario(ctx, image, chars)

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
        await ctx.send("Processing...")
        image, chars = await self.bot.loop.run_in_executor(None, self._move_character, guild_id, channel_id, name,
                                                           movement)
        await post_scenario(ctx, image, chars)

    @command(aliases=['sc', 'savecharacter', 'savechar', 'save_char', 'Sc'],
             help="""Saves a character in the permanent database
                    params:
                    name: the name of the character to be saved

                    Examples:
                    ?r.savechar valkor
                    response: confirmation if the char has been saved
                    """,
             )
    async def save_character(self, ctx: Context, name: str, url='', size_x: int = 1, size_y: int = 1):
        """
        "Saves a character in the permanent database
        @param ctx: Context passed by the API
        @param name: the name of the character to be removed
        @param url: url of the character's token
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        await self.bot.loop.run_in_executor(None, self._save_character, guild_id, channel_id, name, url,
                                            (size_x, size_y))
        await ctx.send(
            f'Character **{name}** saved successfully in the database!\n{dontpad.DONTPAD_BASE_URL}{DTRE_URL}/{guild_id}/{channel_id}/chars')

    @command(aliases=['lc', 'listcharacters', 'listchars', 'list_chars', 'Lc'],
             help="""List the names of the characters that are saved in the channel's dataase
                        params:
                        search: The partial or full name of the character to filter the result
    
                        Examples:
                        ?r.listchars
                        response: A list with character names
                        """,
             )
    async def list_characters(self, ctx: Context, search: str = ''):
        """
        List the names of the characters that are saved in the channel's database
        @param ctx: Context passed by the API
        @param search: The partial or full name of the character to filter the result
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        char_data = _get_char_data(guild_id, channel_id)
        message = ''
        for char_name in char_data:
            if search in char_name:
                message += f'- {char_name}\n'
        if message == '':
            if search == '':
                message = "This channel's database is empty"
            else:
                message = f'No character was found with {search}'
        await ctx.send(message)

    @command(aliases=['dc', 'deletecharacter', 'deletechar', 'delete_chars', 'Dc'],
             help="""Deletes a character from the database
                        params:
                        name: the name of the character to be deleted from the database

                        Examples:
                        ?r.dc valkor
                        response: If the character was deleted
                        """,
             )
    async def delete_character(self, ctx: Context, name: str = ''):
        """
        Deletes a character from the database
        @param ctx: Context passed by the API
        @param name: the name of the character to be deleted from the database
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        char_data = _get_char_data(guild_id, channel_id)
        if name not in char_data:
            await ctx.send(f"Character {name} no found in this channel's database")
        else:
            del char_data[name]
            _save_char_data(guild_id, channel_id, char_data)
            await ctx.send(f"Character {name} was deleted successfully from this channel's database")
