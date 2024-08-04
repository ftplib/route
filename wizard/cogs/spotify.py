from __future__ import annotations

from ext.bot import Wizard
from ext.context import Context, Models
from ext.api.spotify import Spotify as API

from discord.ext.commands import (
    Cog,
    group,
    cooldown,
    BucketType as Type
)

from discord import Message, Embed


class Spotify(Cog):
    def __init__(self: Spotify, bot: Wizard) -> None:
        self.bot: Wizard = bot
        self.api = API(self.bot)
        self.icon = "https://static-00.iconduck.com/assets.00/spotify-icon-512x512-6qhm38iz.png"


    @group(
        name = "spotify",
        brief = "Spotify.",
        usage = "<args>",
        example = "nowplaying",
        invoke_without_command = True
    )
    @cooldown(1, 4, Type.user)
    async def spotify(
        self: Spotify,
        ctx: Context
        
    ) -> Message:
        
        return await ctx.help(
            title = "spotify",
            brief = "Spotify.",
            usage = "<args>",
            example = "nowplaying"
        )
    
    
    @spotify.command(
        name = "nowplaying",
        brief = "Now playing..?",
        usage = None,
        example = None,
        aliases = [
            "np"
        ]
    )
    @cooldown(1, 4, Type.user)
    async def nowplaying(
        self: Spotify,
        ctx: Context
        
    ) -> Message:
        
        track = await self.api.fetch(ctx.author)
        
        if not track:
            return await ctx.deny(
                f"Not playing anything **currently**"
            )
          
        return await ctx.send(
            embed = Embed(
                title = "Spotify: Nowplaying",
                description = f"**{track.title}** by **{track.artist}**",
                color = Models.dark_green
                    
            ).set_thumbnail(
                url = track.thumbnail_url
                    
            ).set_footer(
                text = ctx.author.name,
                icon_url = self.icon
            )
        )


async def setup(bot: Wizard) -> Cog:
    return await bot.add_cog(Spotify(bot))