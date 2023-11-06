from yandex_music import Client, Playlist, Track, TrackShort


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YandexMusicClient(metaclass=Singleton):
    def __init__(self, token: str = None):  # type: ignore
        self.token = token
        self.client: Client = self.initialize_client()

    def initialize_client(self) -> Client:
        client = Client(self.token)
        return client.init()

    def get_playlists(self) -> list[Playlist]:
        return self.client.users_playlists_list()

    def get_likes(self) -> list[TrackShort]:
        likes_song = self.client.users_likes_tracks()
        if likes_song is None:
            raise AttributeError("Client not logged")
        return likes_song.tracks

    def search_tracks(self, query: str) -> list[Track]:
        search_result = self.client.search(query, type_="track")
        return search_result.tracks.results

    def add_to_favorites(self, track_id: str) -> bool:
        operation_result = self.client.users_likes_tracks_add(track_id)
        return operation_result

    def remove_from_favorites(self, track_id: str) -> bool:
        operation_result = self.client.users_likes_tracks_remove(track_id)
        return operation_result
