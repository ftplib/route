from __future__ import annotations

from aiohttp import ClientSession
from typing import Any, Union, List


class Spotify:
    def __init__(self: Spotify, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1/"


    async def _get(
        self: Spotify,
        endpoint: str,
        params: dict = None
    
    ) -> Union[dict, None]:
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        async with ClientSession() as session:
            async with session.get(
                self.base_url + endpoint,
                headers=headers,
                params=params
            ) as response:
                
                if response.status != 200:
                    raise Exception(
                        f"Error {response.status}: {await response.text()}"
                    )
                
                return await response.json()


    async def get_user_info(
        self: Spotify,
        user_id: str
    
    ) -> Profile:
        
        endpoint = f"users/{user_id}"
        data = await self._get(endpoint)
        
        return Profile(
            display_name=data.get('display_name', ''),
            username=data['id'],
            playcount=None,  # Spotify API does not provide playcount directly
            registered=None,  # Spotify API does not provide registration date
            country=data.get('country', ''),
            avatar_url=data['images'][0]['url'] if data['images'] else None
        )

    async def get_recent_tracks(
        self: Spotify,
        user_id: str,
        limit: int = 5
    
    ) -> List[Tracks]:
        
        endpoint = f"users/{user_id}/player/recently-played"
        params = {
            "limit": limit
        }
        data = await self._get(endpoint, params=params)
        
        return [Tracks(
            name=track['track']['name'],
            artist_name=track['track']['artists'][0]['name'],
            album_name=track['track']['album']['name'],
            thumbnail=track['track']['album']['images'][1]['url'] if track['track']['album']['images'] else None
        ) for track in data['items']]


class Profile:
    def __init__(
        self,
        display_name: str = None,
        username: str = None,
        playcount: int = None,
        registered: str = None,
        country: str = None,
        avatar_url: str = None
    ):
        self.display_name = display_name
        self.username = username
        self.playcount = playcount
        self.registered = registered
        self.country = country
        self.avatar_url = avatar_url

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
