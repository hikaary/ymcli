from textual.message import Message
from textual.widgets import Label, Static
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


class Notification(Static):
    class Update(Message):
        def __init__(self, text: str):
            self.text = text
            super().__init__()

    def __init__(self) -> None:
        super().__init__(
            id="notification",
        )
