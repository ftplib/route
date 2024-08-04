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
        
        self.token = "..."

    async def setup_hook(self) -> None:
        await self.load_extensions()
    
    
    async def load_extensions(self) -> None:
        # List of cogs to load
        cogs = [
            "cogs.lastfm",
            # Add other cogs here
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
            except Exception as e:
                print(str(e))
           
           
    async def get_context(
        self, 
        message, *,  
        cls = Context
        
    ) -> Message:

        return await super().get_context(
            message, 
            cls = cls
        )
        
        

    def run(self: Route) -> None:
        super().run(
            token = self.token, 
            reconnect = True, 
            root_logger = True
        )