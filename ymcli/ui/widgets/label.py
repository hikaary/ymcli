from textual.widgets import Label
from yandex_music.track.track import Track


def seconds_to_minutes(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


class TrackInfo(Label):
    def update_track_info(self, track: Track):
        duration = seconds_to_minutes(track.duration_ms // 1000)  # type: ignore
        track_info = f"""
        Название: {track.title}

        Исполнитель: {", ".join(track.artists_name())}
        Длительность: {duration}
        """
        self.update(track_info)
