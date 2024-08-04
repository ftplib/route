from __future__ import annotations

from discord.ext.commands import Bot
from discord import Intents, Message

from .context import Context
from .database import Database as data


class Wizard(Bot):
    def __init__(self: Wizard) -> None:
        super().__init__(
            command_prefix = ",",
            intents = Intents.all(),
            help_command = None
        )
        self.token = "..."


    async def setup_hook(self) -> None:
        await self.load_extensions()
        data().create_table()
    
    
    async def load_extensions(self) -> None:
        cogs = [
            "cogs.lastfm",
            "cogs.spotify",
            "cogs.developer",
            "cogs.event"
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


    def run(self: Wizard) -> None:
        super().run(
            token = self.token, 
            reconnect = True, 
            root_logger = True
        )