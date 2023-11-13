import npyscreen


class MultiLineActionBox(npyscreen.BoxTitle):
    _contained_widgets = npyscreen.MultiLineAction

    def when_cursor_moved(self):
        if hasattr(self.parent, "when_cursor_moved"):
            self.parent.when_cursor_moved()

    def when_value_edited(self):
        if self.entry_widget.value is not None:
            self.parent.when_select()


class PagerBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager
