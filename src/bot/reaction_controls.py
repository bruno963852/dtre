from discord import Reaction

from src.bot import bot


@bot.event
async def on_reaction_add(reaction: Reaction, user):
    if user.id == bot.user.id:
        return

