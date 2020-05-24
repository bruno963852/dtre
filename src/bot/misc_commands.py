from discord.ext.commands import Cog, command, Context


class MiscCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def rualive(self, ctx: Context):
        await ctx.send("Yes, i am alive!")