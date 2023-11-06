import npyscreen
from yandex_music_client import YandexMusicClient


class PlaylistsForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.name = "Playlists"
        self.playlists_list = self.add(
            npyscreen.MultiLineAction,
            name="Playlists",
            max_height=10,
            actionHighlighted=self.on_playlist_selected,
        )

        self.ym_client = YandexMusicClient()

    def beforeEditing(self):
        self.update_playlists()

    def update_playlists(self):
        playlists = self.ym_client.get_playlists()
        likes = self.ym_client.get_likes()
        result_playlist = [
            (f"{playlist.title} - {playlist.track_count} tracks")
            for playlist in playlists
        ]
        result_likes = f"Love - {len(likes)} tracks"

        self.playlists_list.values = [result_likes] + result_playlist

    def on_playlist_selected(self, keypress):
        pass

    def while_editing(self, *args):
        if args[0] == "^P":
            self.playlists_list.h_cursor_line_up()
        elif args[0] == "^N":
            self.playlists_list.h_cursor_line_down()


class SearchForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.name = "Search"
        self.query_field = self.add(npyscreen.TitleText, name="Query")
        self.results_list = self.add(
            npyscreen.MultiLineAction,
            name="Results",
            max_height=10,
            actionHighlighted=self.on_track_selected,
        )
        self.ym_client = YandexMusicClient()

    def on_ok(self):
        query = self.query_field.value
        self.update_results(query)

    def update_results(self, query):
        tracks = self.ym_client.search_tracks(query)
        self.results_list.values = [
            (f"{track.title} by {track.artist} - {track.album}") for track in tracks
        ]
        self.display()

    def on_track_selected(self, keypress):
        # Handle track selection
        pass


class NowPlayingForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.name = "Now Playing"
        self.track_title = self.add(
            npyscreen.TitleFixedText, name="Track", value="No track playing"
        )
        self.progress_bar = self.add(npyscreen.SliderPercent, out_of=100, value=0)
        self.ym_client = YandexMusicClient()

    def update_now_playing(self, track):
        self.track_title.value = f"{track.title} by {track.artist} - {track.album}"
        self.display()

    def update_progress(self, progress):
        self.progress_bar.value = progress
        self.display()


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PlaylistsForm)
        self.addForm("SEARCH", SearchForm)
        self.addForm("NOW_PLAYING", NowPlayingForm)

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
