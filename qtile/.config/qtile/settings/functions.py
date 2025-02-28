import json
import os
import shlex

from libqtile import qtile
from libqtile.config import Key, KeyChord, Match
from libqtile.lazy import lazy

from .path import qtile_scripts_path


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


def move_to_top_right(window, padding_x=15, padding_y=50):
    screen = window.qtile.current_screen
    x = screen.x + screen.width - window.width - padding_x
    y = screen.y + padding_y
    window.set_position_floating(x, y)


def maximize_by_switching_layout():
    def __inner(_qtile):
        current_layout_name = _qtile.current_group.layout.name
        if current_layout_name == 'columns':
            _qtile.current_group.use_layout(1)
        elif current_layout_name == 'max':
            _qtile.current_group.use_layout(2)
        elif current_layout_name == 'treetab':
            _qtile.current_group.use_layout(1)

    return __inner


def toggle_tree_tab_layout():
    def __inner(_qtile):
        current_layout_name = _qtile.current_group.layout.name
        if current_layout_name == 'columns':
            _qtile.current_group.use_layout(3)
        elif current_layout_name == 'max':
            _qtile.current_group.use_layout(3)
        elif current_layout_name == 'treetab':
            _qtile.current_group.use_layout(2)

    return __inner


def create_app_keys(_mod: str, _key, app, wm_class, description):
    return [
        Key([_mod], _key, lazy.function(switch_or_run(app, wm_class)), desc=f"Launch {description}"),
        Key([_mod, "shift"], _key, lazy.function(move_to_screen_or_run(app, wm_class)),
            desc=f"Move {description} to current screen"),
        Key([_mod, "control", "shift"], _key, lazy.spawn(app), desc=f"Launch new instance of {description}")
    ]


def launch_terminal_app(_mod: list[str], _key, app, wm_class, description):
    command = "kitty --title={} --class={} -e {}".format(description, wm_class, app)
    base_mod = _mod if isinstance(_mod, list) else [_mod]
    return [
        Key(
            base_mod,
            _key,
            lazy.function(move_to_screen_or_run(command, wm_class)),
            desc="Launch {}".format(description)
        )
    ]


def next_layout():
    def __inner(_qtile):
        for _i in range(1, 4):
            if _qtile.current_group.current_layout == _i:
                _qtile.current_group.use_layout(_i + 1 if _i < 3 else 1)
                break

    return __inner


def spawn_chord_info(chord: KeyChord):
    def __inner(_qtile):
        """
        Extract the chord's name and its keys' descriptions from the KeyChord instance,
        then spawn the PyQt5 info window passing the data as a JSON argument.
        """
        chord_name = chord.name if chord.name else "KeyChord Info"
        key_entries = []
        for cmd in chord.submappings:
            key_desc = getattr(cmd, "desc", "")
            if cmd.key == "Escape":
                key_desc = "Cancel"
            key_entries.append({"key": cmd.key, "desc": key_desc})
        chord_info = {"name": chord_name, "keys": key_entries}
        chord_info_json = json.dumps(chord_info)
        safe_json = shlex.quote(chord_info_json)
        chord_info_path = os.path.join(qtile_scripts_path, 'chord_info.py')
        _qtile.spawn(f"python3 {chord_info_path} {safe_json}")

    return __inner
