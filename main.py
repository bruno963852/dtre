import json
import os
import random
import traceback

import discord
from discord.ext import commands

from custom_exceptions import InvalidMovementException
from grid import Grid

TOKEN = os.environ["DISCORD_TOKEN"]

GRIDS_FOLDER = 'grids/'

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix=('?ttt.', '!ttt.'), description=description)

grids = dict()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(aliases=['c', 'criar'])
async def create(ctx: commands.Context, height: int, widht: int):
    """
    Cria um mapa com altura e largura.
    Ex: !ttt.create 10 10
    Cria um mapada de altura 10 e largura 10
    ATENCÃO: Isso irá sobreescrever o mapa já existente
    """
    try:
        grids[ctx.guild.id] = Grid(height, widht)
        await ctx.send(grids[ctx.guild.id].to_string())
    except Exception as e:
        print(e.message)
        await ctx.send("Deu erro nessa Shibata")

@bot.command(aliases=['s', 'mostrar'])
async def show(ctx: commands.Context):
    try:
        if ctx.guild.id in grids:
            await ctx.send(grids[ctx.guild.id].to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa Shibata")

@bot.command(aliases=['ae', 'adicionarinimigo', 'adinimigo'])
async def addenemy(ctx, name, pos_x, pos_y, size_x=1, size_y=1):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if grid.has_entity(name):
                await ctx.send("Seu retardado, já tem um aliado ou inimigo chamado {}".format(name))
                return
            grid.add_enemy(name, int(pos_x), int(pos_y), int(size_x), int(size_y))
            await ctx.send(grids[ctx.guild.id].to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['re', 'removerinimigo', 'reminimigo'])
async def removeenemy(ctx, name):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if not grid.has_entity(name):
                await ctx.send("Seu retardado, não existe um aliado ou inimigo chamado {}".format(name))
                return
            grid.remove_enemy(name)
            await ctx.send(grid.to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['ra', 'removeraliado', 'remaliado'])
async def removeally(ctx, name):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if not grid.has_entity(name):
                await ctx.send("Seu retardado, não existe um aliado ou inimigo chamado {}".format(name))
                return
            grid.remove_ally(name)
            await ctx.send(grid.to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['aa', 'adicionaraliado', 'adaliado'])
async def addally(ctx, name, pos_x, pos_y, size_x=1, size_y=1):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if grid.has_entity(name):
                await ctx.send("Seu retardado, já tem um aliado ou inimigo chamado {}".format(name))
                return
            grid.add_ally(name, int(pos_x), int(pos_y), int(size_x), int(size_y))
            await ctx.send(grid.to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['mt', 'movepara'])
async def moveto(ctx, name, pos_x, pos_y):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if grid.can_move_to(name, int(pos_x), int(pos_y)):
                grid.move_to(name, int(pos_x), int(pos_y))
                await ctx.send(grid.to_string())
            else:
                await ctx.send("Movimento inválido")
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")

    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['mb', 'movepor', 'mp'])
async def moveby(ctx, name, movement):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            grid.move_by(name, movement)
            await ctx.send(grid.to_string())
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")
    except InvalidMovementException:
        await ctx.send("Movimento inválido")
    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['sv', 'salvar'])
async def save(ctx):
    try:
        if ctx.guild.id in grids:
            grid = grids[ctx.guild.id] #type: Grid
            if not os.path.exists(GRIDS_FOLDER):
                os.makedirs(GRIDS_FOLDER)
            file = open(GRIDS_FOLDER + str(ctx.guild.id) + '.ttt', 'w')
            json.dump(grid.to_dict(), file)
            file.close()
            await ctx.send("Mapa Salvo com sucesso!!!")
        else:
            await ctx.send("Ainda não há um mapa criado para esse servidor...")

    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['l', 'carregar', 'cr'])
async def load(ctx):
    try:
        if not os.path.exists(GRIDS_FOLDER):
            os.makedirs(GRIDS_FOLDER)
        file = open(GRIDS_FOLDER + str(ctx.guild.id) + '.ttt', 'r')
        grid_dict = json.load(file)
        file.close()
        grids[ctx.guild.id] = Grid.from_dict(grid_dict)
        await ctx.send("Carregando Mapa Salvo...")
        await ctx.send(grids[ctx.guild.id].to_string())

    except Exception as e:
        traceback.print_exc()
        await ctx.send("Deu erro nessa shibata!!!!")

@bot.command(aliases=['t', 'teste'])
async def test(ctx, mod, dc=''):
    mod = int(mod)
    if not dc == '':
        dc = int(dc)
        die = random.randint(1, 20)
        result = ''
        if die == 1:
            result = "Falha Crítica! Vacilou otário!"
        elif die == 20:
            result = "Acerto Crítico! Mete a pêa!"
        elif die + mod >= dc:
            result = "Passou!"
        else:
            result = "NÃO Passou...."
        await ctx.send("Dado: *{}* Mod: *{}* CD: *{}*\nTotal: *{}*\n**{}**".format(die, mod, dc, die+mod, result))
    else:
        die = random.randint(1, 20)
        await ctx.send("Dado: *{}* Mod: *{}\nTotal: **{}**".format(die, mod, die+mod))

bot.run(TOKEN)
