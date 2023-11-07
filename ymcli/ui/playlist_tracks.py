import npyscreen
from yandex_music import Track


class MultiLineAction(npyscreen.BoxTitle):
    _contained_widgets = npyscreen.MultiLineAction

    def h_cursor_line_up(self, *args, **keywords):
        super(MultiLineAction, self).h_cursor_line_up(  # type:ignore
            *args,
            **keywords,
        )
        self.when_cursor_moved()

    def h_cursor_line_down(self, *args, **keywords):
        super(MultiLineAction, self).h_cursor_line_down(  # type:ignore
            *args,
            **keywords,
        )
        self.when_cursor_moved()

    def when_cursor_moved(self):
        self.parent.update_track_info()


class Pager(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class PlaylistTracksForm(npyscreen.FormBaseNew):
    def create(self):
        self.tracks: list[Track] | None = None
        y, x = self.useable_space()
        tracks_list_widht = x - int(x / 3)
        tracks_list_height = y - int(y / 8)
        self.tracks_list = self.add(
            MultiLineAction,
            values=[],
            relx=2,
            rely=2,
            max_width=tracks_list_widht,
            max_height=tracks_list_height,
        )
        self.tracks_list.actionHighlighted = self.select_track

        self.track_info = self.add(
            Pager,
            relx=tracks_list_widht + int(x / 20),
            rely=2,
            max_height=tracks_list_height,
        )

    def beforeEditing(self):
        if self.tracks is None or len(self.tracks) == 0:
            npyscreen.notify_confirm("Not found tracks")
            self.parentApp.switchForm("MAIN")
            return
        self.update_tacks_list()
        self.update_track_info()

    def update_tacks_list(self):
        assert self.tracks is not None

        for track in self.tracks:
            if track is None:
                track_name = "Error load track"
            else:
                artists = ",".join(track.artists_name())
                track_name = f"{track.title} - {artists}"
            self.tracks_list.values.append(track_name)

        self.tracks_list.display()

    def update_track_info(self):
        selected_index = self.tracks_list.entry_widget.cursor_line
        if selected_index is None:
            return
        track = self.tracks[selected_index]
        if track is None:
            track_info = ["Error load track info"]
        else:
            duration = seconds_to_minutes(track.duration_ms // 1000)
            track_info = [
                "Название: " + track.title,
                "Исполнитель: " + ", ".join(track.artists_name()),
                "Длительность: " + duration,
            ]

        self.track_info.values = track_info
        self.track_info.display()

    def select_track(self, act_on_this, key_press):
        npyscreen.notify_confirm("Track selected")


def seconds_to_minutes(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
