from qtile_extras.popup import PopupGridLayout, PopupText

from .theme import theme


class ChordPopupManager:
    def __init__(self, qtile):
        self.qtile = qtile
        self.popup = None

    def show(self, chord_info):
        title_text = chord_info.get("name", "KeyChord Info")
        keys = chord_info.get("keys", [])
        popup_width = 300
        popup_height = 50 + len(keys) * 25 + 15
        total_rows = 1 + len(keys)

        controls = [
            PopupText(
                foreground=theme.foreground,
                text=title_text,
                row=0,
                col=0,
                row_span=1,
                col_span=1,
                h_align="center",
                fontsize=14
            )
        ]

        for i, key_entry in enumerate(keys):
            text = f"{key_entry['key']}: {key_entry['desc']}"
            controls.append(
                PopupText(
                    foreground=theme.subtext0,
                    text=text,
                    row=i + 1,
                    col=0,
                    row_span=1,
                    col_span=1,
                    h_align="center",
                    fontsize=12
                )
            )

        self.popup = PopupGridLayout(
            self.qtile,
            rows=total_rows,
            cols=1,
            width=popup_width,
            height=popup_height,
            controls=controls,
            border=theme.teal,
            border_width=2,
            background=theme.crust,
            opacity=0.8,
            close_on_click=False,
            initial_focus=None,
        )
        self.popup.show(centered=True)

    def kill(self):
        if self.popup is not None:
            self.popup.kill()
            self.popup = None
