from __future__ import annotations

from discord.ext.commands import Bot
from discord import Intents, Message

from .context import Context
from typing import Union


class Route(Bot):
    def __init__(self: Route) -> None:
        
        super().__init__(
            
            command_prefix = ",",
            intents = Intents.all(),
            help_command = None
            
        )
        
        self.cogs = {
            "cogs.lastfm"
        }
        
        self.token = ...
        
        
    async def setup_hook(self) -> None:
        return await self.walk_commands()
    
    
    async def walk_commands(self) -> None:
       for cog in self.cogs:
           await self.load_extension(cog)
           
           
    async def get_context(
        self: Route,
        message: Message, *,
        cls: Context
        
    ) -> Union[Message, Context]:
        
        return await super().get_context(
            origin = message,
            cls = cls
        )
        

    def run(self: Route) -> None:
        super().run(
            token = self.token, 
            reconnect = True, 
            root_logger = True
        )
