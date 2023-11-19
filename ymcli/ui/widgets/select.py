from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option, Separator
from yandex_music import Track, TrackShort

from ...config import CONTROL_PLAYER_BINDINGS, SELECT_BINDINGS
from ...player import Player, TrackInfoUpdate
from ...yandex_music_client import YandexMusicClient


class BaseSelect(OptionList):
    def __init__(
        self,
        *content,
        id=None,
    ):
        super().__init__(
            *content,
            id=id,
        )
        self.player = Player()
        self.ym_client = YandexMusicClient()

    BINDINGS = SELECT_BINDINGS

    def watch_show_vertical_scrollbar(self):
        self.show_vertical_scrollbar = False

    async def action_exit(self) -> None:
        likes_tracks = await self.ym_client.get_likes()
        self.player.playlists = [likes_tracks, likes_tracks]
        playlists = await self.ym_client.get_playlists()
        for playlist in playlists:
            self.player.playlists.append(playlist)
        self.highlighted = None
        self.app.switch_mode("main")


class Playlists(BaseSelect):
    class UpdateTracks(Message):
        def __init__(self, track_list=None) -> None:
            self.track_list = track_list
            super().__init__()

    async def action_select(self) -> None:
        if self.highlighted is None:
            return

        if self.highlighted == 0:
            self.app.switch_mode("stations_list")
            return

        playlist = self.player.playlists[self.highlighted]

        playlist_tracks: list[TrackShort] | list[
            Track
        ] = await playlist.fetch_tracks_async()

        if isinstance(playlist_tracks[0], TrackShort):
            playlist_tracks = [
                short_track.track for short_track in playlist_tracks  # type: ignore
            ]

        self.post_message(self.UpdateTracks(playlist_tracks))
        self.player.track_list = playlist_tracks  # type: ignore
        self.app.switch_mode("playlist")


class TrackList(BaseSelect):
    BINDINGS = CONTROL_PLAYER_BINDINGS

    def action_cursor_up(self) -> None:
        super().action_cursor_up()
        track = self.player.track_list[self.highlighted]  # type: ignore
        self.app.post_message(TrackInfoUpdate(track, "playlist_track_info"))

    def action_cursor_down(self) -> None:
        super().action_cursor_down()
        track = self.player.track_list[self.highlighted]  # type: ignore
        self.app.post_message(TrackInfoUpdate(track, "playlist_track_info"))

    async def action_select(self) -> None:
        if self.highlighted is None:
            return
        await self.player.play(track=self.player.track_list[self.highlighted])

    def update_track_list(self, track_list):
        self.clear_options()
        name_tracks = []
        for track in track_list:
            artists = ",".join(track.artists_name())
            track_name = f"{track.title} - {artists}"
            name_tracks.append(Option(track_name))
            name_tracks.append(Separator())

        self.add_options(name_tracks)


class Stations(BaseSelect):
    def __init__(
        self,
        *content,
        **kwargs,
    ):
        super().__init__(
            *content,
            **kwargs,
        )
        self.ym_client = YandexMusicClient()
        self.player = Player()
        self.radio = self.ym_client.radio

    async def action_select(self) -> None:
        if self.highlighted is None:
            return
        station = self.player.stations[self.highlighted].station

        load_indicatopr = self.app.query_one("LoadingIndicator")
        load_indicatopr.styles.visibility = "visible"
        track: Track = await self.radio.get_first_track(
            station_id=f"{station.id.type}:{station.id.tag}",
            station_from=station.id_for_from,
        )
        await self.player.play(track=track)
        self.app.switch_mode("station_track")
        self.post_message(TrackInfoUpdate(track, "station_track_info"))
