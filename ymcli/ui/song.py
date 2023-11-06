import npyscreen
from yandex_music_client import YandexMusicClient


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
