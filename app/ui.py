import npyscreen
from yandex_music.utils.request_async import asyncio
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

    def beforeEditing(self):
        self.update_playlists()

    def update_playlists(self):
        asyncio.run(self.async_update_playlists())

    async def async_update_playlists(self):
        yandex_music_client = YandexMusicClient()
        playlists = await yandex_music_client.get_playlists()
        self.playlists_list.values = [
            (f"{playlist.title} - {playlist.track_count} tracks")
            for playlist in playlists
        ]

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

    def on_track_selected(self, keypress):
        # Handle track selection
        pass


class NowPlayingForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.name = "Now Playing"
        self.track_title = self.add(npyscreen.TitleFixedText, name="Track")
        self.progress_bar = self.add(npyscreen.SliderPercent, out_of=100, value=0)


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PlaylistsForm)
        self.addForm("SEARCH", SearchForm)
        self.addForm("NOW_PLAYING", NowPlayingForm)

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
