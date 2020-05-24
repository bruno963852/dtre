import traceback

from discord import File
from discord.ext.commands import Cog, command, Context

from src.image.exceptions import CharacterNotFoundException, InvalidMovementException
from src.scenario import Scenario
from src.scenario.scenarios import Scenarios


class CharacterCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['ac', 'addcharacter', 'addchar', 'add_char'])
    async def add_character(self, ctx: Context, name: str, position_x: int, position_y: int, url: str = ''):
        try:
            guild_id = str(ctx.guild.id)
            if url == '':
                attachments = ctx.message.attachments
                if len(attachments) > 0:
                    url = attachments[0].url
            scenario = Scenarios.get_scenario(guild_id)
            await ctx.send("Processando...")
            scenario.add_character(name, url, (position_x, position_y))
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except KeyError:
            await ctx.send("Ainda não há um mapa criado nesse servidor...")
            traceback.print_exc()
        except ValueError:
            await ctx.send("Erro na interpretação do comando...")
            traceback.print_exc()

    @command(aliases=['rc', 'removecharacter', 'removechar', 'remove_char'])
    async def remove_character(self, ctx: Context, name: str):
        try:
            guild_id = str(ctx.guild.id)
            scenario = Scenarios.get_scenario(guild_id)
            await ctx.send("Processando...")
            scenario.remove_character(name)
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except CharacterNotFoundException:
            await ctx.send("Token {} não encontrado".format(name))
        except KeyError:
            await ctx.send("Ainda não há um mapa criado nesse servidor...")
            traceback.print_exc()
        except ValueError:
            await ctx.send("Erro na interpretação do comando...")
            traceback.print_exc()

    @command(aliases=['m', 'mc', 'move_char', 'movecharacter'])
    async def move_character(self, ctx: Context, name: str, movement: str):
        try:
            guild_id = str(ctx.guild.id)
            scenario = Scenarios.get_scenario(guild_id)
            await ctx.send("Processando...")
            scenario.move_character(name, movement)
            await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
        except KeyError:
            await ctx.send("Ainda não há um mapa criado nesse servidor...")
            traceback.print_exc()
        except CharacterNotFoundException:
            await ctx.send("Token {} não encontrado".format(name))
        except InvalidMovementException:
            await ctx.send("Movimento Inválido")
        except ValueError:
            await ctx.send("Erro na interpretação do comando...")
            traceback.print_exc()
