from yandex_music import ClientAsync, Playlist, Track, TracksList

from .config import MUSIC_DIR
from .radio import Radio


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YandexMusicClient(metaclass=Singleton):
    def __init__(
        self,
        client: ClientAsync | None = None,
        radio: Radio | None = None,
    ):
        self.client: ClientAsync | None = client
        self.radio: Radio | None = radio

    @classmethod
    async def initialize_client(cls, token):
        if token is None:
            raise AttributeError("Token not found")

        client = ClientAsync(token)
        await client.init()
        radio = Radio(client)
        cls(client, radio)

    async def get_playlists(self) -> list[Playlist]:
        return await self.client.users_playlists_list()

    async def get_likes(self) -> TracksList:
        likes_song = await self.client.users_likes_tracks()

        if likes_song is None:
            raise AttributeError("Client not logged")
        return likes_song

    async def search_tracks(self, query: str) -> list[Track]:
        search_result = await self.client.search(query, type_="track")
        return search_result.tracks.results

    async def download(self, track: Track):
        await track.download_async(MUSIC_DIR + str(track.id) + ".mp3")

    async def like_track(self, track: Track):
        await track.like_async()

    async def dislike_track(self, track: Track):
        await track.dislike_async()
