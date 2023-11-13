import threading
import time

import npyscreen
from npyscreen.fmForm import FormBaseNew
from yandex_music import Track

from ...player import Player
from ..func import seconds_to_minutes


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


list_widget_type = tuple[
    npyscreen.TitleFixedText,
    npyscreen.Slider,
    npyscreen.Textfield,
]


class ProgressBar(metaclass=Singleton):
    def __init__(self):
        self.player = Player()
        self.running = False
        self.forms: list[str] = []
        self.widgets_list: list[list_widget_type] = []
        self.active_form = ""

    def add_widgets(
        self,
        form: FormBaseNew,
        max_x: int,
    ) -> "ProgressBar":
        assert form.name

        progress_bar_width = max_x - int(max_x / 7)
        bar_title = form.add(
            npyscreen.TitleFixedText,
            name="Track",
            value="No track playing",
            rely=-5,
        )
        progress_bar = form.add(
            npyscreen.Slider,
            value=0,
            label=False,
            max_width=progress_bar_width,
            rely=-3,
        )
        progress_text = form.add(
            npyscreen.Textfield,
            value="00:00 / 00:00",
            rely=-3,
            relx=-18,
        )
        self.forms.append(form.name)
        self.widgets_list.append(
            (  # type: ignore
                bar_title,
                progress_bar,
                progress_text,
            )
        )
        return self

    def start(self):
        self._start_progress_thread()

    def stop(self):
        self._stop_progress_thread()

    def _start_progress_thread(self):
        self.running = True
        self.progress_thread = threading.Thread(
            target=self._progress_update_loop,
            daemon=True,
        )
        self.progress_thread.start()

    def _stop_progress_thread(self):
        self.running = False
        if self.progress_thread.is_alive():
            self.progress_thread.join()

    def _progress_update_loop(self):
        last_time = time.perf_counter()
        while self.running:
            current_time = time.perf_counter()
            elapsed = current_time - last_time

            if self.active_form not in self.forms:
                time.sleep(0.01)
                continue
            if elapsed >= 1.0:
                active_form_index = self.forms.index(self.active_form)

                bar_title, progress_bar, progress_text = self.widgets_list[
                    active_form_index
                ]
                position = self.player.get_position()
                current_track = self.player.get_current_track()
                if current_track and position is not None:
                    duration_seconds = current_track.duration_ms // 1000  # type: ignore
                    absolute_position = int(position * duration_seconds)
                    self._update_bar_info(
                        track=current_track,
                        duration_seconds=duration_seconds,
                        absolute_position=absolute_position,
                        progress_bar=progress_bar,
                        progress_text=progress_text,
                        bar_title=bar_title,
                    )

                last_time = current_time

            time.sleep(0.01)

    def _update_bar_info(
        self,
        duration_seconds: int,
        absolute_position: int,
        track: Track,
        progress_bar,
        progress_text,
        bar_title,
    ):
        progress_bar.out_of = duration_seconds
        progress_bar.value = absolute_position

        current_time_formatted = seconds_to_minutes(absolute_position)
        duration_formatted = seconds_to_minutes(duration_seconds)
        progress_text.value = f"{current_time_formatted} / {duration_formatted}"

        bar_title.value = f"{track.title} by {', '.join(track.artists_name())}"

        bar_title.update()
        progress_text.display()
        progress_bar.display()
