from __future__ import annotations
from typing import Any

from discord.ext.commands import (
    Cog,
    MissingRequiredArgument,
    CommandError,
    CommandNotFound,
    MissingPermissions,
)

from discord import Message

from ext.bot import Wizard
from ext.context import Context


class Event(Cog):
    def __init__(self: Event, bot: Wizard) -> None:
        self.bot: Wizard = bot

    @Cog.listener()
    async def on_command_error(
        self: Event, 
        ctx: Context, 
        error: Any
        
    ) -> Message:

        if isinstance(error, MissingRequiredArgument):
            if ctx.command:
                await ctx.help(
                    title=ctx.command.name,
                    brief=ctx.command.brief,
                    usage=ctx.command.usage,
                    example=getattr(
                        ctx.command, 
                        "__original_kwargs__", {}).get(
                        "example", ""
                    ),
                )

        elif isinstance(error, CommandNotFound):
            return

        elif isinstance(error, CommandError):
            return await ctx.alert("**" 
                + str(error) 
                + "**"
            )

        elif isinstance(error, MissingPermissions):
            return await ctx.alert("**" 
                + "Missing required permissions!" 
                + "**"
            )


async def setup(bot: Wizard) -> Cog:
    await bot.add_cog(Event(bot))