import traceback

from discord import File
from discord.ext.commands import Cog, command, Context

from src.image.exceptions import CharacterNotFoundException, InvalidMovementException
from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


class CharacterCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['ac', 'addcharacter', 'addchar', 'add_char'],
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
                            size_x: int = 1, size_y: int = 2):
        """
        Adds a character to the scenario
        @param ctx: the context passed by the API
        @param name: Name of the character
        @param position_x: position for the character token in the map on the x axis (from left)
        @param position_y: position for the character token in the map on the y axis (from top)
        @param url: url of the image to be used as token (The image will be resized and cropped to a circle and put in
        a frame)
        @param size_x: the size in map squares of the token in the x axis (not supported yet, omit this parameter)
        @param size_y: the size in map squares of the token in the y axis (not supported yet, omit this parameter)
        @return: None
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        await ctx.send("Processando...")
        scenario.add_character(name, url, (position_x, position_y))
        await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))

    @command(aliases=['rc', 'removecharacter', 'removechar', 'remove_char'],
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
        @param ctx: Context passed by the API
        @param name: the name of the character to be removed
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        scenario = Scenarios.get_scenario(guild_id, channel_id)
        await ctx.send("Processando...")
        scenario.remove_character(name)
        await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))

    @command(aliases=['m', 'mc', 'move_char', 'movecharacter', 'move'],
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
        await ctx.send("Processando...")
        scenario.move_character(name, movement)
        await ctx.send(file=File(scenario.get_image(True), filename='play_mat.png'))
