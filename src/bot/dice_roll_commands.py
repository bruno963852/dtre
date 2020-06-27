from discord.ext.commands import Cog, command, Context
from xdice import Pattern, PatternScore


class DiceRollCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['r', 'R'],
             help="""Makes a dice roll indicated by the sent string in dice notation.
                For more info on dice notatio check:
                https://xdice.readthedocs.io/en/latest/dice_notation.html
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
        result = Pattern(roll).roll()
        message = f'__Roll:__ {result.format()}\n__Result:__ **{result}**\n'
        if target > 0:
            message += f'__Target:__ {target}\n**{"Passed!" if result >= target else "Fail..."}**'
        await ctx.send(message)

    @command(aliases=['rd', 'rolld20', 'Rd'],
             help="""Makes a test on d20 system and D&D derivatives's style.
                    Rolls 1d20 + [modifier] and checks against the [target]
                    It also tells if the roll was a critical hit or fumble

                    Examples:
                    ?r.rd 4 15
                    ?r.rd -4
                    response: The result of the roll, with all the details.
                    """,
             )
    async def roll_d20(self, ctx: Context, mod: int = 0, target: int = 0):
        mmod = f'+{mod}' if mod != 0 else ''
        result = Pattern(f'1d20{mmod}').roll()  # type: PatternScore
        message = f'__Roll:__ {result.format()}\n__Result:__ **{result}**\n'
        if result.scores()[0] == 20:
            message += 'You scored a **CRITICAL HIT!!!**'
        elif result.scores()[0] == 1:
            message += 'Too bad... a *Critical Fumble...*'
        elif target > 0:
            message += f'__Target:__ {target}\n**{"Passed!" if result >= target else "Fail..."}**'
        await ctx.send(message)

    @command(aliases=['rp', 'rollpathfinder', 'Rp'],
             help="""Makes a test on Pathfinder 2e system or alikes
                        Rolls 1d20 + [modifier] and checks against the [target]
                        It also tells if the roll was a critical hit or fumble
                        
                        Examples:
                        ?r.rd 4 15
                        ?r.rd -4
                        response: The result of the roll, with all the details.
                        """,
             )
    async def roll_pathfinder(self, ctx: Context, mod: int = 0, target: int = 0):
        mmod = f'+{mod}' if mod != 0 else ''
        result = Pattern(f'1d20{mmod}').roll()  # type: PatternScore
        message = f'__Roll:__ {result.format()}\n__Result:__ **{result}**\n'
        if result.scores()[0] == 20 or (target > 0 and result.scores()[0] - target >= 10):
            message += 'You scored a **CRITICAL HIT!!!**'
        elif result.scores()[0] == 1 or (target > 0 and target - result.scores()[0] >= 10):
            message += 'Too bad... a *Critical Fumble...*'
        elif target > 0:
            message += f'__Target:__ {target}\n**{"Passed!" if result >= target else "Fail..."}**'
        await ctx.send(message)