from __future__ import annotations

from aiohttp import ClientSession
from typing import Any, Union, List
from datetime import datetime


class LastFM:
    def __init__(self: LastFM, api_key: str = None):
        self.api_key = api_key or None
        self.base_url = "http://ws.audioscrobbler.com/2.0/"


    async def _get(
        self: LastFM, 
        params: dict
        
    ) -> Union[dict, None]:
        
        async with ClientSession() as session:
            async with session.get(
                self.base_url, 
                params=params
            ) as response:
                
                if response.status != 200:
                    raise Exception(
                        response.status
                    )
                
                return await response.json()

    async def get_user_info(
        self: LastFM, 
        username: str
        
    ) -> Profile:
        
        params = {
            "method": "user.getinfo",
            "user": username,
            "api_key": self.api_key,
            "format": "json"
        }
        data = await self._get(params)
        user = data['user']

        return Profile(
            display_name=user.get('realname', ''),
            username=user['name'],
            playcount=user['playcount'],
            registered=user['registered']['#text'],
            country=user.get('country', ''),
            avatar_url=user['image'][2]['#text']
        )


    async def get_recent_tracks(
        self: LastFM, 
        username: str, 
        limit: int = 5
        
    ) -> List[Tracks]:
        
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": self.api_key,
            "format": "json",
            "limit": limit
        }
        data = await self._get(params)
        tracks = data['recenttracks']['track']
        return [Tracks(
                    name=track['name'],
                    artist_name=track['artist']['#text'],
                    album_name=track['album']['#text'],
                    thumbnail=track['image'][2]['#text'] if track['image'] else None
                ) for track in tracks]


class Profile:
    def __init__(
        self, 
        display_name: str = None, 
        username: str = None, 
        playcount: int = None, 
        registered: str = None, 
        country: str = "USA", 
        avatar_url: str = None
    ):
        self.display_name = display_name if display_name else username
        self.username = username
        self.playcount = playcount
        self.registered = self.format_date(registered)
        self.country = country
        self.avatar_url = avatar_url
        self.name_url = f"https://www.last.fm/user/{username}"


    def format_date(self, date_value: Union[str, int]) -> str:
        if date_value:
            try:
                if isinstance(date_value, int):
                    date_value = str(date_value)

                if date_value.isdigit():
                    date_obj = datetime.fromtimestamp(int(date_value))
                else:
                    date_obj = datetime.strptime(date_value, '%d %b %Y, %H:%M')
                    
                return date_obj.strftime('%Y-%m-%d')

            except ValueError:
                return date_value
            
        return None


class Tracks:
    def __init__(
        self, 
        name: str = None, 
        artist_name: str = None, 
        album_name: str = None, 
        thumbnail: str = None
    ):
        self.name = name
        self.artist_name = artist_name
        self.album_name = album_name
        self.thumbnail = thumbnail
        
        self.name_url = f"https://www.last.fm/music/{artist_name}/_/{name}"
        self.album_url = f"https://www.last.fm/music/{artist_name}/{album_name}"
        self.artist_url = f"https://www.last.fm/music/{artist_name}"