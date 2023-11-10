import npyscreen
from yandex_music import Playlist, Track, TrackShort, TracksList

from ..yandex_music_client import YandexMusicClient


class PlaylistsForm(npyscreen.FormBaseNew):
    def create(self):
        self.name = "Playlists"
        self.playlist_ui = self.add(
            npyscreen.MultiLineAction,
            name="Playlists",
        )
        self.playlist_ui.actionHighlighted = self.actionHighlighted

        self.ym_client = YandexMusicClient()

    def beforeEditing(self):
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

        self.playlist_ui.values = playlists_names
        self.playlist_ui.playlists = playlists

    def actionHighlighted(self, act_on_this, key_press):
        playlist: Playlist | TracksList = self.playlist_ui.playlists[
            self.playlist_ui.cursor_line
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
