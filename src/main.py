import os
import traceback
from typing import Dict

from discord import File
from discord.ext import commands
from discord.ext.commands import CheckFailure

from src.image.exceptions import CharacterNotFoundException, InvalidMovementException, FrameWithoutAlphaException
from src.scenario import Scenario

TOKEN = os.environ["DISCORD_TOKEN"]

GRIDS_FOLDER = 'grids/'

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix=('?drpg.', '!dprg.', '?r.', '!r.'), description=description)

scenarios: Dict[str, Scenario] = {}


@bot.event
async def on_ready():
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


@bot.command(aliases=['t'])
async def test(ctx: commands.Context):
    await ctx.send("Eu tô funcionando!")


@bot.command(aliases=['c'])
async def create(ctx: commands.Context, name: str, offset_x: int, offset_y: int, square_size: int, url: str = ''):
    try:
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        guild_id = str(ctx.guild.id)
        await ctx.send("Processando...")
        scenario = Scenario(guild_id, name=name, map_url=url, offset_pixels=(offset_x, offset_y),
                            square_size=square_size)
        scenarios[guild_id] = scenario
        await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
    except KeyError:
        traceback.print_exc()
    except ValueError:
        traceback.print_exc()


@bot.command(aliases=['ac', 'addcharacter', 'addchar', 'add_char'])
async def add_character(ctx: commands.Context, name: str, position_x: int, position_y: int, url: str = ''):
    try:
        guild_id = str(ctx.guild.id)
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        scenario = scenarios[guild_id]
        await ctx.send("Processando...")
        scenario.add_character(name, url, (position_x, position_y))
        await ctx.send(file=File(scenario.get_image(), filename='play_mat.png'))
    except KeyError:
        await ctx.send("Ainda não há um mapa criado nesse servidor...")
        traceback.print_exc()
    except ValueError:
        await ctx.send("Erro na interpretação do comando...")
        traceback.print_exc()


@bot.command(aliases=['rc', 'removecharacter', 'removechar', 'remove_char'])
async def remove_character(ctx: commands.Context, name: str):
    try:
        guild_id = str(ctx.guild.id)
        scenario = scenarios[guild_id]
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


@bot.command(aliases=['m', 'mc', 'move_char', 'movecharacter'])
async def move_character(ctx: commands.Context, name: str, movement: str):
    try:
        guild_id = str(ctx.guild.id)
        scenario = scenarios[guild_id]
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

bot.run(TOKEN)
