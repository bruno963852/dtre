import json
import os
import random
import traceback
from typing import List, Dict, Tuple

import discord
from discord import File, Member, Permissions
from discord.abc import GuildChannel
from discord.ext import commands
from discord.ext.commands import CheckFailure

from play_mat.exceptions import TokenNotFoundException, InvalidMovementException, FrameWithoutAlphaException

# TOKEN = os.environ["DISCORD_TOKEN"]
from play_mat import PlayMat

TOKEN = "NzA4NDI3MjExNzk5MDAzMTY3.XsCMUQ.mLC28t-V_f1_f05FD4zBqViTySg"
GRIDS_FOLDER = 'grids/'

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix=('?drpg.', '!dprg.', '?r.', '!r.'), description=description)

maps: Dict[str, PlayMat] = {}


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
    await ctx.message.delete()
    return True


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print(error)
    if error is CheckFailure:
        await ctx.send("Erro, o bot não tem as permissões necessárias...")
    else:
        await ctx.send("Houve um erro inesperado...")


@bot.command(aliases=['t'])
async def test(ctx: commands.Context):
    await ctx.send("Eu tô funcionando!")


@bot.command(aliases=['c'])
async def create(ctx: commands.Context, offset_x: int, offset_y: int, square_size: int, url: str = ''):
    try:
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        guild_id = str(ctx.guild.id)
        await ctx.send("Processando...")
        playmat = PlayMat(guild_id, url, (offset_x, offset_y), square_size)
        maps[guild_id] = playmat
        await ctx.send(file=File(playmat.get_map(), filename='play_mat.png'))
    except KeyError:
        traceback.print_exc()
    except ValueError:
        traceback.print_exc()


@bot.command(aliases=['at'])
async def addtoken(ctx: commands.Context, name: str, position_x: int, position_y: int, url: str = ''):
    try:
        guild_id = str(ctx.guild.id)
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        playmat = maps[guild_id]
        await ctx.send("Processando...")
        playmat.add_token(name, url, (position_x, position_y))
        await ctx.send(file=File(playmat.get_map(), filename='play_mat.png'))
    except KeyError:
        await ctx.send("Ainda não há um mapa criado nesse servidor...")
        traceback.print_exc()
    except ValueError:
        await ctx.send("Erro na interpretação do comando...")
        traceback.print_exc()


@bot.command(aliases=['rt'])
async def removetoken(ctx: commands.Context, name: str):
    try:
        guild_id = str(ctx.guild.id)
        playmat = maps[guild_id]
        await ctx.send("Processando...")
        playmat.remove_token(name)
        await ctx.send(file=File(playmat.get_map(), filename='play_mat.png'))
    except TokenNotFoundException:
        await ctx.send("Token {} não encontrado".format(name))
    except KeyError:
        await ctx.send("Ainda não há um mapa criado nesse servidor...")
        traceback.print_exc()
    except ValueError:
        await ctx.send("Erro na interpretação do comando...")
        traceback.print_exc()


@bot.command(aliases=['st'])
async def setframe(ctx: commands.Context, name: str, url: str = ''):
    try:
        guild_id = str(ctx.guild.id)
        if url == '':
            attachments = ctx.message.attachments
            if len(attachments) > 0:
                url = attachments[0].url
        playmat = maps[guild_id]
        await ctx.send("Processando...")
        playmat.set_frame(name, url)
        await ctx.send(file=File(playmat.get_map(), filename='play_mat.png'))
    except KeyError:
        await ctx.send("Ainda não há um mapa criado nesse servidor...")
        traceback.print_exc()
    except ValueError:
        await ctx.send("Erro na interpretação do comando...")
        traceback.print_exc()
    except FrameWithoutAlphaException:
        await ctx.send("Erro, o frame tem que ter um canal de transparência (imagem no formato png)...")
        traceback.print_exc()


@bot.command(aliases=['m'])
async def move(ctx: commands.Context, name: str, movement: str):
    try:
        guild_id = str(ctx.guild.id)
        playmat = maps[guild_id]
        await ctx.send("Processando...")
        playmat.move_token(name, movement)
        await ctx.send(file=File(playmat.get_map(), filename='play_mat.png'))
    except KeyError:
        await ctx.send("Ainda não há um mapa criado nesse servidor...")
        traceback.print_exc()
    except TokenNotFoundException:
        await ctx.send("Token {} não encontrado".format(name))
    except InvalidMovementException:
        await ctx.send("Movimento Inválido")
    except ValueError:
        await ctx.send("Erro na interpretação do comando...")
        traceback.print_exc()


bot.run(TOKEN)
