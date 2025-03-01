from qtile_extras.popup import PopupRelativeLayout, PopupText


class ChordPopupManager:
    def __init__(self, qtile):
        self.qtile = qtile
        self.popup = None

    def show_chord_info(self, chord_info):
        controls = [PopupText(
            text=chord_info.get("name", "KeyChord Info"),
            pos_x=0.05, pos_y=0.05,
            width=0.9, height=0.2,
            h_align="center",
            fontsize=16
        )]

        keys = chord_info.get("keys", [])
        base_y = 0.3
        height_per_item = 0.1
        for i, key_entry in enumerate(keys):
            text = f"{key_entry['key']}: {key_entry['desc']}"
            controls.append(
                PopupText(
                    text=text,
                    pos_x=0.1, pos_y=base_y + i * height_per_item,
                    width=0.8, height=height_per_item,
                    h_align="center",
                    fontsize=12
                )
            )

        popup_height = 150 + len(keys) * 30
        self.popup = PopupRelativeLayout(
            self.qtile,
            width=300,
            height=popup_height,
            controls=controls,
            background="1e1e2e60",
            close_on_click=False,
            initial_focus=None,
        )
        self.popup.show(centered=True)

    def kill_popup(self):
        if self.popup is not None:
            self.popup.kill()
            self.popup = None
