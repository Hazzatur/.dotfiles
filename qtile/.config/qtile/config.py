import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "kitty"
laptop = os.path.exists('/sys/class/power_supply/BAT1/status')
wallpaper_path = '~/.wallpaper/disperse01.jpg' if laptop else '~/.wallpaper/disperse02.jpg'
wallpaper = os.path.expanduser(wallpaper_path)

keys = [
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -modi drun -show drun -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Application launcher"),
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
    # Apps
    Key([mod], "b", lazy.spawn("opera"), desc="Launch Opera"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Launch Thunar"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Launch Flameshot"),
    Key(["control", "mod1"], "Delete", lazy.spawn("kitty -e btop"), desc="Launch Btop")
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# Widgets
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

widgets = [
    widget.CurrentLayout(),
    widget.GroupBox(),
    widget.Prompt(),
    widget.WindowName(),
    widget.Chord(
        chords_colors={
            "launch": ("#282A36", "#282A36"),
        },
        name_transform=lambda name: name.upper(),
    ),
    widget.Systray(),
    widget.Clock(format="%a %d-%m-%Y %I:%M %p"),
]

if laptop:
    widgets.append(widget.BatteryIcon())
    widgets.append(widget.Battery(format="{char} {percent:2.0%}"))

widgets.append(widget.QuickExit())


# Screens

# Transparency
# 100% — FF
# 95% — F2
# 90% — E6
# 85% — D9
# 80% — CC
# 75% — BF
# 70% — B3
# 65% — A6
# 60% — 99
# 55% — 8C
# 50% — 80
# 45% — 73
# 40% — 66
# 35% — 59
# 30% — 4D
# 25% — 40
# 20% — 33
# 15% — 26
# 10% — 1A
# 5% — 0D
# 0% — 00

def create_screen(x=0, y=0, width=1920, height=1080, main=False, wallpaper_mode='stretch'):
    bottom_bar = bar.Bar(
        widgets=widgets,
        size=24,
        background=["#00000000", "#00000000"],
        opacity=1.0
    ) if main else None

    return Screen(
        wallpaper=wallpaper,
        wallpaper_mode=wallpaper_mode,
        x=x,
        y=y,
        width=width,
        height=height,
        bottom=bottom_bar
    )


screen_configs = [
    {'x': 1920, 'y': 1080, 'width': 1440, 'height': 900, 'main': True},  # DP-1
    {'x': 0, 'y': 180},  # HDMI-0
    {'x': 1920, 'y': 0},  # DP-3
    {'x': 3840, 'y': 100, 'width': 1080, 'height': 1920, 'wallpaper_mode': 'fill'}  # DP-4
]

if laptop:
    screens = [create_screen(0, 0, 1920, 1080, True)]
else:
    screens = [create_screen(**config) for config in screen_configs]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
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
