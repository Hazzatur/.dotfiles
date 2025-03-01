from qtile_extras.popup import PopupAbsoluteLayout, PopupText

from .theme import theme


class ChordPopupManager:
    def __init__(self, qtile):
        self.qtile = qtile
        self.popup = None

    def show_chord_info(self, chord_info):
        title_text = chord_info.get("name", "KeyChord Info")
        keys = chord_info.get("keys", [])
        popup_width = 300
        popup_height = 50 + len(keys) * 25 + 15

        controls = [
            PopupText(
                foreground=theme.foreground,
                text=title_text,
                pos_x=15,
                pos_y=10,
                width=popup_width - 30,
                height=30,
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
                    pos_x=15,
                    pos_y=50 + i * 25,
                    width=popup_width - 30,
                    height=25,
                    h_align="center",
                    fontsize=12
                )
            )

        self.popup = PopupAbsoluteLayout(
            self.qtile,
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

    def kill_popup(self):
        if self.popup is not None:
            self.popup.kill()
            self.popup = None
