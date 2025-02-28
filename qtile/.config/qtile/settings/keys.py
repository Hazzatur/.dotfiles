import os

from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy

from .functions import create_app_keys, launch_terminal_app, maximize_by_switching_layout, next_layout, toggle_copyq, \
    toggle_tree_tab_layout
from .path import qtile_scripts_path

alt = "mod1"
mod = "mod4"

audio_key_chord = KeyChord(
    [mod], "a", [
        Key([], "t", lazy.spawn(os.path.join(qtile_scripts_path, 'toggle_audio.py')),
            desc="Toggle Audio"),
        Key([], "y", lazy.spawn("xdg-open https://music.youtube.com"),
            desc="Open YT Music"),
        Key([], "s", lazy.spawn("xdg-open https://open.spotify.com"),
            desc="Open Spotify"),
        Key([], "p", lazy.spawn("pavucontrol"),
            desc="Open PulseAudio Volume Control")
    ],
    mode=False,
    name="Audio Controls"
)

keys = [
    # Lock screen
    Key([mod], "escape", lazy.spawn(os.path.join(qtile_scripts_path, 'lock.sh')), desc="Lock screen"),
    # Qtile controls
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift", "control"], "h", lazy.layout.swap_column_left(), desc="Swap column with left/right"),
    Key([mod, "shift", "control"], "l", lazy.layout.swap_column_right(), desc="Swap column with left/right"),
    Key([mod, alt], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "n", lazy.layout.normalize()),
    # Layout and window controls
    Key([mod, "shift"], "Tab", lazy.function(next_layout()), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.function(maximize_by_switching_layout()), desc="Toggle maximize"),
    Key([mod, "control"], "f", lazy.function(toggle_tree_tab_layout()), desc="Toggle maximize"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    # Rofi
    Key([mod], "r", lazy.spawn("rofi -show drun -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Application launcher"),
    Key([mod], "d", lazy.spawn("rofi -show run -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Run prompt"),
    Key([mod], "Tab", lazy.spawn("rofi -show window -config ~/.config/rofi/rofidmenu.rasi"),
        desc="Switch windows"),
    # Audio
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 1%+"), desc="Raise Volume by 1%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 1%-"), desc="Lower Volume by 1%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    audio_key_chord,
    # Multimedia
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn(os.path.join(qtile_scripts_path, 'brightness.sh up')),
        desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn(os.path.join(qtile_scripts_path, 'brightness.sh down')),
        desc="Decrease brightness"),
    # Media keys
    Key([], "XF86Explorer", lazy.spawn("xdg-open ."), desc="Open file manager"),
    Key([], "XF86Calculator", lazy.spawn("qalculate-qt"), desc="Launch Qalculate!"),
    Key([], "XF86Mail", lazy.spawn("thunderbird"), desc="Launch Thunderbird"),
    Key([], "XF86HomePage", lazy.spawn("google-chrome-stable"), desc="Launch Chrome"),
    # Screenshots
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Launch Flameshot"),
    # Clipboard
    Key([mod], "v", lazy.function(toggle_copyq()), desc="Toggle CopyQ"),
    # Apps
    *create_app_keys(mod, "Return", "kitty", "kitty", "Kitty"),
    *create_app_keys(mod, "b", "vivaldi", "vivaldi-stable", "Vivaldi"),
    *create_app_keys(mod, "e", "thunar", "thunar", "Thunar"),
    *launch_terminal_app([mod, "control"], "e", "yazi", "yazi", "Yazi"),
    *launch_terminal_app(["control", "mod1"], "Delete", "btop", "btop", "Btop")
]

key_chords = {chord.name: chord for chord in keys if isinstance(chord, KeyChord)}
