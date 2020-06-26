import json
from typing import Tuple

from discord import File
from discord.ext.commands import Cog, command, Context, Bot

from src.bot import dontpad
from src.bot.common import post_scenario
from src.bot.common_functions import get_attachment
from src.bot.dontpad import DTRE_URL
from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


class ScenarioCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _create_scenario(guild_id, channel_id, name, url, offset_x, offset_y, square_size) -> Tuple[File, dict]:
        scenario = Scenario(guild_id, channel_id, name=name, map_url=url, offset_pixels=(offset_x, offset_y),
                            square_size=square_size)
        Scenarios.put_scenario(guild_id, channel_id, scenario)
        return File(scenario.get_image(), filename='play_mat.png'), scenario.characters

    @staticmethod
    def _save_scenario(guild_id, channel_id, url: str):
        scenario_dict = Scenarios.get_scenario(guild_id, channel_id).dict
        scenario_json = json.dumps(scenario_dict)
        dontpad.write(url, scenario_json)

    @staticmethod
    def _load_scenario_dontpad(guild_id, channel_id, dontpad_url) -> Tuple[File, dict]:
        dontpad_content = dontpad.read(dontpad_url)
        dict_ = json.loads(dontpad_content)
        scenario = Scenario.from_dict(dict_, guild_id, channel_id)
        Scenarios.put_scenario(guild_id, channel_id, scenario)
        return File(scenario.get_image(), filename='play_mat.png'), scenario.characters

    @staticmethod
    def _load_scenario_json(guild_id, channel_id, json_str) -> Tuple[File, dict]:
        dict_ = json.loads(json_str)
        scenario = Scenario.from_dict(dict_, guild_id, channel_id)
        Scenarios.put_scenario(guild_id, channel_id, scenario)
        return File(scenario.get_image(), filename='play_mat.png'), scenario.characters

    @command(aliases=['c', 'C'],
             help="""Creates a scenario with the specified name
                params:
                name: Name of the map
                square_size: Size of the squares in the map in pixels
                url: Url of the map image
                offset_x: Offset in pixels for starting drawing the squares from the left side
                offset_y: Offset in pixels for starting drawing the squares from the top side
                
                Examples:
                ?r.c mydungeon
                ?r.c "just a bridge" 45 https://i.imgur.com/G5kc4QX.jpg 17 17
                response: The map of the scenario. If only the name is passed, the default map is created
                """,
             )
    async def create(self, ctx: Context, name: str = 'unnamed lands', square_size: int = 64, url: str = '',
                     offset_x: int = 0,
                     offset_y: int = 0):
        """
        Creates a scenario with the specified name
        Examples:
        ?r.c mydungeon
        ?r.c "just a bridge" 45 https://i.imgur.com/G5kc4QX.jpg 17 17
        response: The map of the scenario. If only the name is passed, the default map is created
        @param ctx: Context passed by the API
        @param name: Name of the map
        @param square_size: Size of the squares in the map in pixels
        @param url: Url of the map image
        @param offset_x: Offset in pixels for starting drawing the squares from the left side
        @param offset_y: Offset in pixels for starting drawing the squares from the top side
        @return: None
        """
        url = get_attachment(ctx, url)
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        image, chars = await self.bot.loop.run_in_executor(None, self._create_scenario, guild_id, channel_id, name, url,
                                                           offset_x, offset_y, square_size)
        await post_scenario(ctx, image, chars)

    @command(aliases=['s', 'S'],
             help="""Saves the scenario in json form to be loaded later. The json is posted in a dontpad url

                Examples:
                ?r.s
                ?r.save
                response: The json of the scenario
                """,
             )
    async def save(self, ctx: Context):
        """
        Saves the scenario in json form to be loaded later. The json is posted in a dontpad url
        @param ctx: Context passed by the API
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        url = f'{DTRE_URL}/{guild_id}/{channel_id}/'
        await ctx.send("Processing...")
        await self.bot.loop.run_in_executor(None, self._save_scenario, guild_id, channel_id, url)
        await ctx.send(f'Json of the scenario saved in {dontpad.DONTPAD_BASE_URL + url}')

    @command(aliases=['l', 'L'],
             help="""Loads the scenario from a dontpad url

                    params:
                    dontpad_url: the dontpad url from which the json will be loaded. If no url specified, the engine loads from the default url for this channel

                    Examples: 
                    '''
                    ?r.l http://dontpad.com/dtre_scenarios/720610147814211605/720610147814211608/
                    ?r.l
                    '''
                    """
             )
    async def load(self, ctx: Context, dontpad_url: str = ''):
        """
        Loads the scenario from a dontpad url
        @param ctx: Context passed by the API
        @param dontpad_url: the dontpad url from which the json will be loaded
        @return:
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        if dontpad_url == '':
            dontpad_url = f'{DTRE_URL}/{guild_id}/{channel_id}/'
        elif dontpad.DONTPAD_BASE_URL in dontpad_url:
            dontpad_url = dontpad_url[len(dontpad.DONTPAD_BASE_URL):]
        await ctx.send("Processing...")
        image, chars = await self.bot.loop.run_in_executor(None, self._load_scenario_dontpad, guild_id, channel_id,
                                                           dontpad_url)
        await post_scenario(ctx, image, chars)

    @command(aliases=['lj', 'loadjson', 'Lj'],
             help="""Loads the scenario from a json
             
                params:
                json_str: the json to be loaded. it can have spaces and you dont need to add ""

                Examples: ?r.lj {"name": "teste", "map": {"image_url": null, "offset": [0, 0], "square_size": 
                64}, "characters": [{"name": "zezo", "token": {"position": [8, 2], "image_url": 
                "https://i.pinimg.com/originals/f1/77/53/f177537621e9225d22b87f3269afb901.jpg", "frame_url": 
                "image/files/default_token_frame.png"}}, {"name": "g3", "token": {"position": [15, 4], "image_url": 
                "https://starfinderwiki.com/mediawikisf/images/thumb/8/8d/Space_goblin.jpg/250px-Space_goblin.jpg", 
                "frame_url": "image/files/default_token_frame.png"}}]} ?r.save response: The json of the scenario , 
                """
             )
    async def load_json(self, ctx: Context, *, json_str: str):
        """
        Loads the scenario from a json
        @param ctx: Context passed by the API
        @param json_str: the json to be loaded.
        @return:
        """
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        await ctx.send("Processing...")
        image, chars = await self.bot.loop.run_in_executor(None, self._load_scenario_json, guild_id, channel_id, json_str)
        await post_scenario(ctx, image, chars)
