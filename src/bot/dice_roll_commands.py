from discord.ext.commands import Cog, command, Context
from dice_parser import DiceParser, ParseResult


class DiceRollCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser = DiceParser()

    @command(aliases=['r'],
             help="""Makes a dice roll indicated by the sent string in dice roll notation
                xdy±z -> where "x" is the quantity of dice, "y" is how many face the dice have
                and you can add or subtract a modifier "z"
                params:
                roll: the dice roll to be made in dice notation
                target: (Optional) the target value to be obtained, the engine will tell if
                the test failed or succeeded
                        
                Examples:
                ?r.roll 1d20+7
                ?r.r 1d20+10 18
                response: The result of the roll, with all the details.
                """,
             )
    async def roll(self, ctx: Context, roll: str, target: int = 0):
        """
        Makes a dice roll indicated by the sent string in dice roll notation
        @param ctx: the context passed by the API
        @param roll: the dice roll in dice notation
        @param target: the target value (Optional)
        """
        result = self.parser.parse(roll)  # type: ParseResult
        message = '__Roll:__ {}\n__Result:__ **{}**\n'.format(result.string, result.value)
        if target > 0:
            message += '__Target:__ {}\n**{}**'.format(target, "Passed!" if result.value >= target else "Fail...")
        await ctx.send(message)
