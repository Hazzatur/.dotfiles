import os
import subprocess

from libqtile import hook, qtile
from libqtile.config import Match

from .functions import center_resize, get_chord_popup_manager, move_to_top_right, spawn_chord_info
from .keys import key_chords
from .path import qtile_scripts_path


@hook.subscribe.client_new
def floating_position(window):
    if hasattr(window, "match"):
        if window.match(Match(wm_class="copyq")):
            center_resize(window, 800, 600)
        elif window.match(Match(wm_class="btop")):
            center_resize(window, 1400, 800)
        elif window.match(Match(wm_class="chord_info")):
            move_to_top_right(window)


@hook.subscribe.enter_chord
def on_enter_chord(chord_name):
    chord = key_chords.get(chord_name)
    if chord:
        spawn_chord_info(chord)(qtile)


@hook.subscribe.leave_chord
def on_leave_chord():
    get_chord_popup_manager(qtile).kill_popup()


@hook.subscribe.startup_once
def autostart():
    subprocess.call(os.path.join(qtile_scripts_path, 'autostart.sh'))
