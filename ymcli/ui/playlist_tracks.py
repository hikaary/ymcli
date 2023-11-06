import npyscreen
from yandex_music import Track


class PlaylistTracksForm(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = ""
        self.CANCEL_BUTTON_TEXT = ""

        self.tracks: list[Track] | None = None
        self.tracks_list = self.add(
            npyscreen.MultiLineAction,
            relx=2,
            rely=2,
            max_width=40,
            value_changed_callback=self.on_track_selected,
        )
        self.tracks_list.values = []

        self.track_info = self.add(
            npyscreen.Pager,
            relx=53,
            rely=2,
        )

    def beforeEditing(self):
        if self.tracks is None or len(self.tracks) == 0:
            npyscreen.notify_confirm("Not found tracks")
            self.parentApp.switchForm("MAIN")
            return

        for track in self.tracks:
            if track is None:
                track_name = "Error load track"
            else:
                artists = ",".join(track.artists_name())
                track_name = f"{track.title} - {artists}"
            self.tracks_list.values.append(track_name)

        self.tracks_list.display()
        self.update_track_info(self.tracks[0])

    def on_track_selected(self, widget):
        if self.tracks is not None and widget.cursor_line < len(self.tracks):
            track = self.tracks[widget.cursor_line]
            self.update_track_info(track)

    def update_track_info(self, track: Track):
        if track is None:
            track_info = ["Error load track info"]
        else:
            track_info = [track.title, f"Artist: {track.artists[0].name}"]

        self.track_info.values = track_info
        self.track_info.display()

    def actionHighlighted(self, act_on_this, key_press):
        pass
