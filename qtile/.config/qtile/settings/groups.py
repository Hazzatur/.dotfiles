from libqtile.config import Group, Key
from libqtile.lazy import lazy

from .keys import keys, mod

groups = [
    Group(name="1", layout="columns", label="1"),
    Group(name="2", layout="columns", label="2"),
    Group(name="3", layout="columns", label="3"),
    Group(name="4", layout="columns", label="4"),
    Group(name="5", layout="columns", label="5"),
    Group(name="6", layout="columns", label="6"),
    Group(name="7", layout="columns", label="7"),
    Group(name="8", layout="columns", label="8"),
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
