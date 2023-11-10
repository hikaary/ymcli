import npyscreen

from ..yandex_music_client import YandexMusicClient


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
