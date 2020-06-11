import traceback
import json

from discord import File
from discord.ext.commands import Cog, command, Context

from src.bot.common_functions import get_attachment
from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


class ScenarioCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['c'],
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
    async def create(self, ctx: Context, name: str, square_size: int = 64, url: str = '', offset_x: int = 0,
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
        try:
            url = get_attachment(ctx, url)
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
            await ctx.send("Processando...")
            scenario = Scenario(guild_id, channel_id, name=name, map_url=url, offset_pixels=(offset_x, offset_y),
                                square_size=square_size)
            Scenarios.put_scenario(guild_id, channel_id,  scenario)
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except KeyError:
            traceback.print_exc()
        except ValueError:
            traceback.print_exc()

    @command(aliases=['s'],
             help="""Saves the scenario in json form to be loaded later

                Examples:
                ?r.s
                ?r.save
                response: The json of the scenario
                """,
             )
    async def save(self, ctx: Context):
        """
        Saves the scenario in json form to be loaded later
        @param ctx: Context passed by the API
        """
        try:
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
            await ctx.send("Processando...")
            d = Scenarios.get_scenario(guild_id, channel_id).dict
            message = "```{}```".format(json.dumps(d))
            await ctx.send(message)
        except KeyError:
            traceback.print_exc()
        except ValueError:
            traceback.print_exc()

    @command(aliases=['l'],
             help="""Loads the scenario from a json
             
                params:
                json_str: the json to be loaded. it can have spaces and you dont need to add ""

                Examples: ?r.l {"name": "teste", "map": {"image_url": null, "offset": [0, 0], "square_size": 
                64}, "characters": [{"name": "zezo", "token": {"position": [8, 2], "image_url": 
                "https://i.pinimg.com/originals/f1/77/53/f177537621e9225d22b87f3269afb901.jpg", "frame_url": 
                "image/files/default_token_frame.png"}}, {"name": "g3", "token": {"position": [15, 4], "image_url": 
                "https://starfinderwiki.com/mediawikisf/images/thumb/8/8d/Space_goblin.jpg/250px-Space_goblin.jpg", 
                "frame_url": "image/files/default_token_frame.png"}}]} ?r.save response: The json of the scenario , 
                """
             )
    async def load(self, ctx: Context, *, json_str: str):
        """
        Loads the scenario from a json
        @param ctx: Context passed by the API
        @param json_str: the json to be loaded.
        @return:
        """
        try:
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
            await ctx.send("Processando...")
            dict_ = json.loads(json_str)
            scenario = Scenario.from_dict(dict_, guild_id, channel_id)
            Scenarios.put_scenario(guild_id, channel_id, scenario)
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except KeyError:
            traceback.print_exc()
        except ValueError:
            traceback.print_exc()
