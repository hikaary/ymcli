import asyncio

from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option, Separator
from yandex_music import Track, TrackShort

from ...config import SELECT_BINDINGS
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

    def action_exit(self) -> None:
        self.highlighted = None
        self.app.switch_mode("main")


class Playlists(BaseSelect):
    class UpdateTracks(Message):
        def __init__(self, track_list) -> None:
            self.track_list = track_list
            super().__init__()

    async def action_select(self) -> None:
        if self.highlighted is None:
            return

        if self.highlighted == 0:
            self.app.switch_mode("stations_list")
            return

        playlist = self.player.playlists[self.highlighted]

        loop = asyncio.get_running_loop()
        playlist_tracks: list[TrackShort] | list[Track] = await loop.run_in_executor(
            None,
            playlist.fetch_tracks,
        )
        if isinstance(playlist_tracks[0], TrackShort):
            playlist_tracks = [
                short_track.track for short_track in playlist_tracks  # type: ignore
            ]

        self.post_message(self.UpdateTracks(playlist_tracks))
        self.player.track_list = playlist_tracks  # type: ignore
        self.app.switch_mode("playlist")


class TrackList(BaseSelect):
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