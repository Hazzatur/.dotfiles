#!/bin/bash

host=$(hostname)

if [[ "$host" = "RED" ]]; then
    xrandr \
    --output HDMI-0 --mode 1920x1080 --pos 0x180 --rotate normal \
    --output HDMI-1 --off \
    --output DP-0 --off \
    --output DP-1 --mode 1440x900 --pos 1920x1080 --rotate normal \
    --output DP-2 --off \
    --output DP-3 --mode 1920x1080 --pos 1920x0 --rotate normal --primary \
    --output DP-4 --mode 1920x1080 --pos 3840x100 --rotate left \
    --output DP-5 --off
elif [[ "$host" = "REDL" ]]; then
    xrandr \
    --output eDP1 --mode 1920x1080 --primary
fi
