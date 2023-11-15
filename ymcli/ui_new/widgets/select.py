from textual.binding import Binding, BindingType
from textual.widgets import OptionList
from yandex_music import Track, TrackShort


class BaseSelect(OptionList):
    BINDINGS: list[BindingType] = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("end", "last", "Last", show=False),
        Binding("enter", "select", "Select", show=False),
        Binding("home", "first", "First", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]


class SelectPlayListTrack(BaseSelect):
    def action_select(self) -> None:
        if self.highlighted is None:
            return

        playlist = self.app.playlists[int(self.highlighted)]  # type: ignore
        playlist_tracks: list[TrackShort] | list[Track] = playlist.fetch_tracks()
        if isinstance(playlist_tracks[0], TrackShort):
            playlist_tracks = [
                short_track.track for short_track in playlist_tracks  # type: ignore
            ]

        self.app.player.track_list = playlist_tracks  # type: ignore
        self.app.switch_mode("playlisttracks")


class SelectPlayTrack(BaseSelect):
    pass
