#!/bin/bash

host=$(hostname)

picom -cb &
numlockx on &
copyq &
flameshot &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
xset s noblank s off -dpms &
dbus-launch dunst --config "$HOME/.config/dunst/dunstrc" &

if [[ "$host" = "REDL" ]]; then
  xautolock -time 10 -locker "$HOME/.config/qtile/scripts/lock.sh" -detectsleep &
fi
