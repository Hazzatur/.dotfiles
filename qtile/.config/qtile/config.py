import os
import subprocess

from libqtile import bar, layout, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


def switch_or_run(app, wm_class):
    def __inner(_qtile):
        for window in _qtile.windows_map.values():
            if hasattr(window, "match") and window.match(Match(wm_class=wm_class)):
                _qtile.current_screen.set_group(window.group)
                return
        _qtile.spawn(app)

    return __inner


def move_to_screen_or_run(app, wm_class):
    def __inner(_qtile):
        for window in _qtile.windows_map.values():
            if hasattr(window, "match") and window.match(Match(wm_class=wm_class)):
                if window.floating:
                    center_resize(window, window.width, window.height)
                else:
                    window.togroup(_qtile.current_group.name, switch_group=True)
                return
        _qtile.spawn(app)

    return __inner


def toggle_copyq():
    def __inner(_qtile):
        for window in _qtile.windows_map.values():
            if hasattr(window, "match") and window.match(Match(wm_class="copyq")):
                _qtile.spawn("copyq hide")
                return
        _qtile.spawn("copyq show")

    return __inner


def center_resize(window, width, height):
    mouse_x, mouse_y = qtile.core.get_mouse_position()
    window.set_size_floating(width, height)
    window.set_position_floating(mouse_x, mouse_y)
    window.center()


@hook.subscribe.client_new
def floating_position(window):
    if hasattr(window, "match"):
        if window.match(Match(wm_class="copyq")):
            center_resize(window, 800, 600)
        elif window.match(Match(wm_class="btop")):
            center_resize(window, 1400, 800)


def maximize_by_switching_layout():
    def __inner(_qtile):
        current_layout_name = _qtile.current_group.layout.name
        if current_layout_name == 'monadtall':
            _qtile.current_group.use_layout(1)
        elif current_layout_name == 'max':
            _qtile.current_group.use_layout(2)

    return __inner


def create_app_keys(_mod, _key, app, wm_class, description):
    return [
        Key([_mod], _key, lazy.function(switch_or_run(app, wm_class)), desc=f"Launch {description}"),
        Key([_mod, "shift"], _key, lazy.function(move_to_screen_or_run(app, wm_class)),
            desc=f"Move {description} to current screen"),
        Key([_mod, "control", "shift"], _key, lazy.spawn(app), desc=f"Launch new instance of {description}")
    ]


mod = "mod4"
terminal = "kitty"
laptop = os.path.exists('/sys/class/power_supply/BAT1/status')
wallpaper_path = '~/.wallpaper/disperse02.jpg' if laptop else '~/.wallpaper/disperse01.jpg'
_wallpaper = os.path.expanduser(wallpaper_path)

keys = [
    # Lock screen
    Key([mod], "escape", lazy.spawn(os.path.expanduser('~/.config/qtile/scripts/lock.sh')), desc="Lock screen"),
    # Qtile controls
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack", ),
    # Layout and window controls
    Key([mod, "shift"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.function(maximize_by_switching_layout()), desc="Toggle maximize"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    # Rofi
    Key([mod], "r", lazy.spawn("rofi -show drun -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Application launcher"),
    Key([mod], "d", lazy.spawn("rofi -show run -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Run prompt"),
    Key([mod], "Tab", lazy.spawn("rofi -show window -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Switch windows"),
    # Sound
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 1%+"), desc="Raise Volume by 1%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 1%-"), desc="Lower Volume by 1%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    Key([mod], "XF86AudioMute", lazy.spawn(os.path.expanduser('~/.config/qtile/scripts/toggle_audio.py')),
        desc="Toggle Audio"),
    # Multimedia
    Key([mod], "XF86AudioPlay", lazy.spawn("xdg-open https://music.youtube.com"), desc="Open YT Music"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn(os.path.expanduser('~/.config/qtile/scripts/brightness.sh up')),
        desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn(os.path.expanduser('~/.config/qtile/scripts/brightness.sh down')),
        desc="Decrease brightness"),
    # Screenshots
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Launch Flameshot"),
    # Clipboard
    Key([mod], "v", lazy.function(toggle_copyq()), desc="Toggle CopyQ"),
    # Apps
    *create_app_keys(mod, "Return", terminal, terminal, "terminal"),
    *create_app_keys(mod, "b", "vivaldi", "vivaldi-stable", "Vivaldi"),
    *create_app_keys(mod, "e", "thunar", "thunar", "Thunar"),
    Key(["control", "mod1"], "Delete",
        lazy.function(move_to_screen_or_run("kitty --title=btop --class=btop -e btop", "btop")), desc="Launch Btop")
]

groups = [
    Group(name="1", layout="monadtall", label="1"),
    Group(name="2", layout="monadtall", label="2"),
    Group(name="3", layout="monadtall", label="3"),
    Group(name="4", layout="monadtall", label="4"),
    Group(name="5", layout="monadtall", label="5"),
    Group(name="6", layout="monadtall", label="6"),
    Group(name="7", layout="monadtall", label="7"),
    Group(name="8", layout="monadtall", label="8"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Move focused window to group {i.name}"
            )
        ]
    )


class CatppuccinMocha:
    background = "#1e1e2e"
    foreground = "#cdd6f4"
    rosewater = "#f5e0dc"
    flamingo = "#f2cdcd"
    pink = "#f5c2e7"
    mauve = "#cba6f7"
    red = "#f38ba8"
    maroon = "#eba0ac"
    peach = "#fab387"
    yellow = "#f9e2af"
    green = "#a6e3a1"
    teal = "#94e2d5"
    sky = "#89dceb"
    sapphire = "#74c7ec"
    blue = "#89b4fa"
    lavender = "#b4befe"
    subtext1 = "#bac2de"
    subtext0 = "#a6adc8"
    overlay2 = "#9399b2"
    overlay1 = "#7f849c"
    overlay0 = "#6c7086"
    surface2 = "#585b70"
    surface1 = "#45475a"
    surface0 = "#313244"
    mantle = "#181825"
    crust = "#11111b"


colors = CatppuccinMocha()

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors.sapphire,
    "border_normal": colors.background
}

layouts = [
    layout.Floating(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.TreeTab(
        font="MesloLGS NF",
        fontsize=12,
        bg_color=colors.background,
        active_bg=colors.sapphire,
        active_fg=colors.surface1,
        inactive_bg=colors.foreground,
        inactive_fg=colors.background,
        urgent_bg=colors.red,
        urgent_fg=colors.background,
        padding_x=0,
        padding_y=8,
        padding_left=0,
        section_bottom=16,
        section_top=16,
        section_left=16,
        section_fg=colors.pink,
        section_fontsize=10,
        vspace=3,
        panel_width=240,
        previous_on_rm=True
    )
]

widget_defaults = dict(
    font="MesloLGS NF",
    fontsize=12,
    padding=0,
    background=colors.background
)

extension_defaults = widget_defaults.copy()


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
                max_chars=60
            ),
            widget.Chord(
                chords_colors={
                    "launch": ("#282A36", "#282A36")
                },
                name_transform=lambda name: name.upper()
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
                    ]
                )
            )
            widgets.append(widget.Spacer(length=8))
            widgets.append(widget.Systray(padding=3))

        widgets.append(widget.Spacer(length=8))
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
        widgets.append(widget.Spacer(length=8))

        if laptop:
            widgets.append(widget.BatteryIcon())
            widgets.append(widget.Battery(format="{char} {percent:2.0%}"))
            widgets.append(widget.Spacer(length=8))

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
            widgets.append(widget.Spacer(length=8))

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
    {'x': 0, 'y': 180, 'wallpaper': "~/Pictures/wallpaper/W2.png"},  # HDMI-0
    {'x': 1920, 'y': 1080, 'width': 1440, 'height': 900, 'main': True, 'wallpaper': "~/Pictures/wallpaper/W3.png"},
    # DP-1
    {'x': 1920, 'y': 0, 'wallpaper': "~/Pictures/wallpaper/W1.png"},  # DP-3
    {'x': 3840, 'y': 100, 'width': 1080, 'height': 1920, 'wallpaper_mode': 'fill',
     'wallpaper': "~/Pictures/wallpaper/1.png"}  # DP-4
]

if laptop:
    screens = [create_screen(0, 0, 1920, 1080, True)]
else:
    screens = [create_screen(**config) for config in screen_configs]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors.sapphire,
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="dialog"),  # dialog boxes
        Match(wm_class="download"),  # downloads
        Match(wm_class="error"),  # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),  # kdenlive
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="notification"),  # notifications
        Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="toolbar"),  # toolbars
        Match(wm_class="Yad"),  # yad boxes
        Match(title="branchdialog"),  # gitk
        Match(title='Confirmation'),  # tastyworks exit box
        Match(title='Qalculate!'),  # qalculate-gtk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="tastycharts"),  # tastytrade pop-out charts
        Match(title="tastytrade"),  # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"),  # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"),  # tastytrade settings
        Match(wm_class="copyq"),  # copyq
        Match(wm_class="btop")  # btop
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.Popen([script])
