import os

from libqtile import bar
from libqtile.config import Screen
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

from .CatppuccinMocha import CatppuccinMocha

laptop = os.path.exists('/sys/class/power_supply/BAT1/status')
wallpaper_path = '~/.wallpaper/disperse02.jpg' if laptop else '~/.wallpaper/disperse01.jpg'
_wallpaper = os.path.expanduser(wallpaper_path)
colors = CatppuccinMocha()


def add_spacer(widgets):
    return widgets.append(widget.Spacer(length=8))


def create_screen(x=0, y=0, width=1920, height=1080, main=False, wallpaper_mode='stretch', wallpaper=_wallpaper):
    def create_widgets():
        widgets = [
            widget.CurrentLayoutIcon(
                foreground=colors.foreground,
                padding=10,
                scale=0.6
            ),
            widget.CurrentLayout(
                foreground=colors.foreground,
                padding=5
            ),
            widget.GroupBox(
                fontsize=11,
                margin_y=5,
                margin_x=5,
                padding_y=0,
                padding_x=1,
                borderwidth=3,
                active=colors.subtext1,
                inactive=colors.overlay1,
                rounded=False,
                highlight_color=colors.surface0,
                highlight_method="line",
                this_current_screen_border=colors.blue,
                this_screen_border=colors.sapphire,
                other_current_screen_border=colors.red,
                other_screen_border=colors.surface1
            ),
            widget.WindowName(
                foreground=colors.subtext1,
                max_chars=60,
                padding=5
            ),
            widget.Chord(
                chords_colors={
                    "launch": ("#282A36", "#282A36")
                },
                name_transform=lambda name: name.upper(),
                padding=10
            )
        ]

        if main:
            widgets.append(
                widget.PulseVolume(
                    foreground=colors.pink,
                    fmt='🕫  Vol: {}',
                    decorations=[
                        BorderDecoration(
                            colour=colors.pink,
                            border_width=[0, 0, 2, 0]
                        )
                    ],
                    padding=10
                )
            )
            widgets.append(widget.Systray(padding=10))

        add_spacer(widgets)

        widgets.append(
            widget.Clock(
                foreground=colors.teal,
                format="⏱  %a %d-%m-%Y %I:%M %p",
                padding=10,
                decorations=[
                    BorderDecoration(
                        colour=colors.teal,
                        border_width=[0, 0, 2, 0]
                    )
                ]
            )
        )

        add_spacer(widgets)

        if laptop:
            widgets.append(widget.BatteryIcon())
            widgets.append(widget.Battery(format="{char} {percent:2.0%}"))
            add_spacer(widgets)

        if main:
            widgets.append(
                widget.QuickExit(
                    foreground=colors.red,
                    fmt='⏻: {}',
                    padding=10,
                    decorations=[
                        BorderDecoration(
                            colour=colors.red,
                            border_width=[0, 0, 2, 0]
                        )
                    ]
                )
            )
        add_spacer(widgets)

        return widgets

    top_bar = bar.Bar(
        widgets=create_widgets(),
        border_color=colors.background,
        border_width=5,
        margin=[8, 8, 0, 8],
        size=26,
        opacity=1.0
    )

    return Screen(
        wallpaper=wallpaper,
        wallpaper_mode=wallpaper_mode,
        x=x,
        y=y,
        width=width,
        height=height,
        top=top_bar
    )


screen_configs = [
    {'x': 1080, 'y': 311},  # DP-3
    {'x': 1080, 'y': 1391, 'width': 1440, 'height': 900, 'main': True},  # DP-1
    {'x': 0, 'y': 0, 'width': 1080, 'height': 1920, 'wallpaper_mode': 'fill'},  # HDMI-0
    {'x': 3000, 'y': 411, 'width': 1080, 'height': 1920, 'wallpaper_mode': 'fill'}  # DP-4
]

if laptop:
    screens = [create_screen(0, 0, 1920, 1080, True)]
else:
    screens = [create_screen(**config) for config in screen_configs]
