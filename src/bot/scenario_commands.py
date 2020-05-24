import traceback

from discord import File
from discord.ext.commands import Cog, command, Context

from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


class ScenarioCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['c'])
    async def create(self, ctx: Context, name: str, offset_x: int = 0, offset_y: int = 0, square_size: int = 0,
                     url: str = ''):
        try:
            if url == '':
                attachments = ctx.message.attachments
                if len(attachments) > 0:
                    url = attachments[0].url
            guild_id = str(ctx.guild.id)
            await ctx.send("Processando...")
            scenario = Scenario(guild_id, name=name, map_url=url, offset_pixels=(offset_x, offset_y),
                                square_size=square_size)
            Scenarios.put_scenario(scenario)
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except KeyError:
            traceback.print_exc()
        except ValueError:
            traceback.print_exc()
