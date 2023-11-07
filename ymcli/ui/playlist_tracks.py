import npyscreen
from yandex_music import Track


class MultiLineAction(npyscreen.MultiLineAction):
    # _contained_widgets = npyscreen.BoxTitle

    def h_cursor_line_up(self, *args, **keywords):
        super(MultiLineAction, self).h_cursor_line_up(*args, **keywords)
        self.when_cursor_moved()

    def h_cursor_line_down(self, *args, **keywords):
        super(MultiLineAction, self).h_cursor_line_down(*args, **keywords)
        self.when_cursor_moved()

    def when_cursor_moved(self):
        self.parent.update_track_info()


class PlaylistTracksForm(npyscreen.FormBaseNew):
    def create(self):
        self.tracks: list[Track] | None = None
        self.tracks_list = self.add(
            MultiLineAction,
            relx=2,
            rely=2,
            max_width=40,
            values=[],
        )
        self.tracks_list.actionHighlighted = self.select_track

        self.track_info = self.add(
            npyscreen.Pager,
            relx=50,
            rely=2,
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
        selected_index = self.tracks_list.cursor_line
        track = self.tracks[selected_index]
        if track is None:
            track_info = ["Error load track info"]
        else:
            track_info = [track.title, track.meta_data]

        self.track_info.values = track_info
        self.track_info.display()

    def select_track(self, act_on_this, key_press):
        npyscreen.notify_confirm("Track selected")
