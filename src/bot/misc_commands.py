from discord.ext.commands import Cog, command, Context


class MiscCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def rualive(self, ctx: Context):
        """
        Just a simple command to test if the bot is alive.
        If he bot is alive, it responds "Yes, I'm alive!"
        """
        await ctx.send("Yes, i am alive!")