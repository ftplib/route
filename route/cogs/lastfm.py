from __future__ import annotations

from ext.bot import Route
from ext.database import Database as data

from ext.context import Context, Models
from ext.api.lastfm import LastFM as API

from discord.ext.commands import (
    Cog,
    group,
    cooldown,
    BucketType as Type
)

from discord import Message, Embed


class LastFM(Cog):
    def __init__(self: LastFM, bot: Route, key) -> None:
        self.bot: Route = bot
        self.api = API(key)
        
        self.icon = "https://cdn1.iconfinder.com/data/icons/somacro___dpi_social_media_icons_by_vervex-dfjq/500/lastfm.png"


    @group(
        name = "lastfm",
        brief = "LastFM",
        usage = "<args>",
        example = "nowplaying",
        invoke_without_command = True,
        aliases = [
            "lf",
            "fm"
        ]
    )
    @cooldown(1, 4, Type.user)
    async def lastfm(
        self: LastFM,
        ctx: Context

    ) -> Message:
        
        return await ctx.help(
            title = "lastfm",
            brief = "LastFM",
            usage = "<args>",
            example = "nowplaying"
        )
    
    
    @lastfm.command(
        name = "link",
        brief = "Link your LF acc",
        usage = "<username>",
        example = "sqlite3",
        aliases = [
            "set"
        ]
    )
    async def link(
        self: LastFM,
        ctx: Context,
        username: str = None
        
    ) -> Message:
        
        await data.link_account(
            self = data,
            id = ctx.author.id,
            username = username
        )
        
        return await ctx.approve(
            content = f"Linked!",
            emoji = Models.lastfm,
            colour = Models.dark_red
        )


    @lastfm.command(
        name = "userinfo",
        usage = "(username)",
        example = "sqlite3",
        aliases = [
            "ui",
            "whois"
        ]
    )
    async def userinfo(
        self: LastFM,
        ctx: Context,
        username: str = None
        
    ) -> Message:
        
        profile = await self.api.get_user_info(username)
        
        return await ctx.send(
            embed = Embed(
                title = f"LastFM: {username}",
                description = (
                    f'```Display: {profile.display_name}\n' + 
                    f'Playcount: {profile.playcount}\n' + 
                    f'Registered: {profile.registered}\n'+ 
                    f'Country: {profile.country}```'
                ),
                color = Models.dark_red
                
            ).set_footer(
                text = f"LastFM - {ctx.author.id}",
                icon_url = self.icon
                
            ).set_thumbnail(
                url = profile.avatar_url
            )
        )


    @lastfm.command(
        name = "recent",
        brief = "View a users recent tracks",
        usage = "(username)",
        example = "sqlite3"
    )
    async def recent(
        self: LastFM,
        ctx: Context,
        username: str = None, *,
        limit: int = 3
        
    ) -> Message:
        
        tracks = await self.api.get_recent_tracks(
            username = username, 
            limit = limit
        )
        
        embed = Embed(
            title = f"LastFM: {username}",
            color = Models.dark_red
        )
        
        for track in tracks:
            
            embed.add_field(
                name = track.name,
                value = (
                    f"Artist: {track.artist_name}\n",
                    f"Album: {tracks.album_name}"
                ),
                inline = False
            )
            
            return await ctx.send(embed = Embed)
    
    
    @lastfm.command(
        name = "nowplaying",
        brief = "Now playing!",
        usage = None,
        example = None,
        aliases = [
            "np"
        ]
    )
    async def nowplaying(
        self: LastFM,
        ctx: Context
        
    ) -> Message:
        
        username = data.get_username(self = data, id = ctx.author.id)
        if not username:
            return await ctx.deny(
                content = f"You do not have a **linked account!**",
                emoji = Models.lastfm,
                colour = Models.dark_red
            )
        
        tracks = await self.api.get_recent_tracks(
            username = username,
            limit = 1 
        )
        
        if not tracks:
            return await ctx.deny(
                f"No recent tracks **found!**"
            )
        
        track = tracks[0]
        return await ctx.send(
            
            embed = Embed(
                title = "LastFM: Nowplaying",
                description = f"**{track.name}** by **{track.artist_name}**",
                color = Models.dark_red
                
            ).set_thumbnail(
                url = track.thumbnail
                
            ).set_footer(
                text = ctx.author.name,
                icon_url = (
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else self.icon
                )
            )
        )


async def setup(bot: Route) -> None:
    cog_instance = LastFM(
        bot=bot, 
        key="..."
    )
    await bot.add_cog(cog_instance)