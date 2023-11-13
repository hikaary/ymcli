from yandex_music import Playlist, Track, TrackShort, TracksList

from ..yandex_music_client import YandexMusicClient
from . import widgets
from .forms import BaseForm


class PlaylistsForm(BaseForm):
    def create(self):
        super().create()
        self.name = "Playlists"
        self.playlist_ui = self.add(
            widgets.MultiLineActionBox,
            name="Playlists",
            max_height=self.max_widgets_height,
        )
        self.bar = self.add_bar()
        self.ym_client = YandexMusicClient()

    def beforeEditing(self):
        self.bar.active_form = self.name
        self.update_playlists()

    def update_playlists(self):
        playlists: list[Playlist] = self.ym_client.get_playlists()
        likes_tracks: TracksList = self.ym_client.get_likes()
        playlists_names = [
            (f"{playlist.title} - {playlist.track_count} tracks")
            for playlist in playlists
        ]
        playlists_names.insert(0, f"Likes - {len(likes_tracks)} tracks")
        playlists.insert(0, likes_tracks)  # type: ignore

        playlists_names.append("Staions")

        self.playlist_ui.values = playlists_names
        self.playlist_ui.playlists = playlists

    def when_select(self):
        if self.playlist_ui.value == len(self.playlist_ui.values) - 1:
            self.parentApp.switchForm("SELECT_STATION")

        playlist: Playlist | TracksList = self.playlist_ui.playlists[
            self.playlist_ui.value
        ]
        playlist_tracks: list[TrackShort] | list[Track] = playlist.fetch_tracks()

        if isinstance(playlist_tracks[0], TrackShort):
            playlist_tracks = [
                short_track.track for short_track in playlist_tracks  # type: ignore
            ]

        self.parentApp.getForm("PLAYLIST_TRACKS").tracks = playlist_tracks
        self.parentApp.getForm("PLAYLIST_TRACKS").name = (
            playlist.title if isinstance(playlist, Playlist) else "Likes"
        )
        self.parentApp.switchForm("PLAYLIST_TRACKS")
        self.playlist_ui.value = None
