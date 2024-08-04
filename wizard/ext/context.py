from __future__ import annotations
from discord.ext.commands import Context

from discord import Embed, Message
from typing import Optional


class Models:
    warn = ""
    tick = ""
    nope = ""
    
    lastfm = "<:lastfm:1269488486117802057>"
    spotify = "<:spotify:1269525780069744744>"
    soundcloud = ""
    
    green = 0xA4EB78
    yellow = 0xFFC64A
    red = 0xF94848
    
    dark_red = 0xD71D28
    dark_green = 0x2BBE58
    

class Context(Context):
    def __init__(self: Context, **kwargs):
        super().__init__(**kwargs)


    async def approve(
        self: Context,
        content: Optional[str] = None,
        emoji: Optional[str] = Models.tick,
        colour: Optional[int] = Models.green,
    ) -> Message:

        return await self.send(
            embed=Embed(
                description=f"{emoji} {self.message.author.mention}: {content}",
                color=colour,
            )
        )


    async def alert(
        self: Context,
        content: Optional[str] = None,
        emoji: Optional[str] = Models.warn,
        colour: Optional[int] = Models.yellow,
    ) -> Message:

        return await self.send(
            embed=Embed(
                description=f"{emoji} {self.message.author.mention}: {content}",
                color=colour,
            )
        )


    async def deny(
        self: Context,
        content: Optional[str] = None,
        emoji: Optional[str] = Models.nope,
        colour: Optional[int] = Models.red,
    ) -> Message:

        return await self.send(
            embed=Embed(
                description=f"{emoji} {self.message.author.mention}: {content}",
                color=colour,
            )
        )


    async def help(
        self: Context,
        title: Optional[str] = None,
        brief: Optional[str] = "...",
        usage: Optional[str] = None,
        example: Optional[str] = None,
    ) -> Message:

        return await self.send(
            embed=Embed(
                title="Command: " + title,
                description=f"Brief: {brief}```Usage: {title} {usage}\nExample: {title} {example}```",
                color=0x69919D,
            )
        )