from .bar import *  # noqa
from .label import *  # noqa
from .radio import *  # noqa
from .select import *  # noqa


class Animation:
    def __init__(self, widget):
        self.widget = widget
        self.widget.styles.visibility = "visible"

    def start(self):
        self.widget.styles.animate(
            "opacity",
            value=100,
            duration=1,
            on_complete=self.second_step,
        )

    def second_step(self):
        self.widget.styles.animate(
            "opacity",
            value=0,
            duration=1,
            on_complete=self.end,
        )

    def end(self):
        self.widget.styles.visibility = "hidden"
