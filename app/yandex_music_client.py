import asyncio

from yandex_music import ClientAsync, Playlist, Track


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YandexMusicClient(metaclass=Singleton):
    def __init__(self, token: str = None):  # type: ignore
        self.token = token
        self.client = None
        asyncio.run(self.initialize_client())

    async def initialize_client(self) -> None:
        self.client = ClientAsync(self.token)
        await self.client.init()

    async def get_playlists(self) -> list[Playlist]:
        user_playlists = await self.client.users_playlists_list()
        return user_playlists

    async def search_tracks(self, query: str) -> list[Track]:
        search_result = await self.client.search(query, type_="track")
        return search_result.tracks.results

    async def add_to_favorites(self, track_id: str) -> bool:
        operation_result = await self.client.users_likes_tracks_add(track_id)
        return operation_result

    async def remove_from_favorites(self, track_id: str) -> bool:
        operation_result = await self.client.users_likes_tracks_remove(track_id)
        return operation_result
