from __future__ import annotations

from typing import Union
from discord import Spotify as DefaultSpotify, Member, utils

from ext.bot import Route
import datetime


class Spotify:
    def __init__(self: Spotify, bot: Route):
        self.bot = bot

    async def fetch(
        self: Spotify, 
        user: Member
        
    ) -> DefaultSpotify:
        
        activity = utils.find(lambda a: isinstance(a, DefaultSpotify), user.activities)
        if activity:
            try:
                return Track(
                    title=activity.title,
                    artist=activity.artist,
                    album=activity.album,
                    track_id=activity.track_id,
                    start=activity.start,
                    end=activity.end,
                    duration=activity.duration,
                    thumbnail_url=activity.album_cover_url
                )
            except Exception as e:
                print(str(e))

class Track:
    def __init__(
        self, 
        title: str, 
        artist: str, 
        album: str, 
        track_id: str, 
        start: datetime, 
        end: datetime, 
        duration: int,
        thumbnail_url: str
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.track_id = track_id
        self.start = start
        self.end = end
        self.duration = duration

        self.track_url = f"https://open.spotify.com/track/{track_id}"
        self.thumbnail_url = thumbnail_url