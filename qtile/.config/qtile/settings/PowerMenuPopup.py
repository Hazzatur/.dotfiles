import os

from libqtile.lazy import lazy
from qtile_extras.popup import PopupAbsoluteLayout, PopupImage, PopupText

from .path import qtile_images_path, qtile_scripts_path
from .theme import theme


class PowerMenuPopup:
    def __init__(self, qtile):
        self.qtile = qtile
        self.popup = None

    def show(self):
        popup_width = 360
        popup_height = 170

        controls = [
            PopupImage(
                filename=os.path.join(qtile_images_path, 'lock.svg'),
                pos_x=15,
                pos_y=20,
                width=100,
                height=100,
                highlight=theme.sapphire,
                highlight_border=5,
                highlight_radius=50,
                mouse_callbacks={
                    "Button1": lazy.spawn(os.path.join(qtile_scripts_path, 'lock.sh'))
                }
            ),
            PopupImage(
                filename=os.path.join(qtile_images_path, 'reboot.svg'),
                pos_x=130,
                pos_y=20,
                width=100,
                height=100,
                highlight=theme.teal,
                highlight_border=5,
                highlight_radius=50,
                mouse_callbacks={
                    "Button1": lazy.spawn("reboot")
                }
            ),
            PopupImage(
                filename=os.path.join(qtile_images_path, 'shutdown.svg'),
                pos_x=245,
                pos_y=20,
                width=100,
                height=100,
                highlight=theme.red,
                highlight_border=5,
                highlight_radius=50,
                mouse_callbacks={
                    "Button1": lazy.spawn("poweroff")
                }
            ),
            PopupText(
                foreground=theme.foreground,
                text="Lock",
                pos_x=15,
                pos_y=130,
                width=100,
                height=20,
                h_align="center",
                fontsize=14
            ),
            PopupText(
                foreground=theme.foreground,
                text="Reboot",
                pos_x=130,
                pos_y=130,
                width=100,
                height=20,
                h_align="center",
                fontsize=14
            ),
            PopupText(
                foreground=theme.foreground,
                text="Shutdown",
                pos_x=245,
                pos_y=130,
                width=100,
                height=20,
                h_align="center",
                fontsize=14
            ),
        ]

        self.popup = PopupAbsoluteLayout(
            self.qtile,
            width=popup_width,
            height=popup_height,
            controls=controls,
            border=theme.teal,
            border_width=2,
            background=theme.crust,
            opacity=0.8,
            initial_focus=None,
        )
        self.popup.show(centered=True)

    def kill(self):
        if self.popup is not None:
            self.popup.kill()
            self.popup = None
