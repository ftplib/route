from __future__ import annotations

from discord import Message
from discord.ext.commands.context import Context

from ext.context import Context
from ext.bot import Wizard

from discord.ext.commands import (
    Cog,
    CommandError as DeveloperOnly,
    group
)


class Developer(Cog):
    def __init__(self: Developer, bot: Wizard) -> None:
        self.bot: Wizard = bot
    
    
    async def cog_check(
        self: Developer, 
        ctx: Context
    ) -> bool:
        if ctx.author.id in [
            1255959858734301277,
            456,
            789
        ]:
            return True
        
        else:
            raise DeveloperOnly(
                "The command is developer only"
            )


    @group(
        name = "developer",
        usage = "<args>",
        example = "reload moderation",
        invoke_without_command = True,
        aliases = [
            "dev",
            "wizard",
            "own"
        ]
    )
    async def developer(
        self: Developer,
        ctx: Context

    ) -> Message:
        
        return await ctx.help(
            name = "developer",
            usage = "<args>",
            example = "reload moderation",
        )


    @developer.command(
        name = "reload",
        brief = "Re-load a Cog",
        usage = "(cog)",
        example = "moderation"
    )
    async def reload(
        self: Developer,
        ctx: Context,
        cog: str
        
    ) -> Message:
        
        try:
    
            await self.bot.reload_extension(
                name = f"cogs.{cog}"
            )
            return await ctx.approve(
                f"Re-Loaded **{cog}**"
            )

        except Exception as e:
            return await ctx.deny(str(e))


async def setup(bot: Wizard) -> Cog:
    return await bot.add_cog(Developer(bot))