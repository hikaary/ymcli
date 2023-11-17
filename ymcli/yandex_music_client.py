import asyncio

from yandex_music import Client, Playlist, Track, TracksList

from .config import MUSIC_DIR
from .radio import Radio


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YandexMusicClient(metaclass=Singleton):
    def __init__(self, token: str | None = None):
        self.token = token
        self.client: Client = self.initialize_client()
        self.radio = Radio(self.client)

    def initialize_client(self) -> Client:
        if self.token is None:
            raise AttributeError("Token not found")

        client = Client(self.token)
        return client.init()

    def get_playlists(self) -> list[Playlist]:
        return self.client.users_playlists_list()

    def get_likes(self) -> TracksList:
        likes_song = self.client.users_likes_tracks()
        if likes_song is None:
            raise AttributeError("Client not logged")
        return likes_song

    def search_tracks(self, query: str) -> list[Track]:
        search_result = self.client.search(query, type_="track")
        return search_result.tracks.results

    async def download(self, track: Track):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            track.download,
            MUSIC_DIR + str(track.id) + ".mp3",
        )

    def like_track(self, track: Track):
        track.like()

    def dislike_track(self, track: Track):
        track.dislike()
