#!/bin/bash

host=$(hostname)

if [[ "$host" = "RED" ]]; then
    xrandr \
    --output HDMI-0 --mode 1920x1080 --pos 0x0 --rotate left  \
    --output HDMI-1 --off \
    --output DP-0 --off \
    --output DP-1 --mode 1440x900 --pos 1080x1391 --rotate normal \
    --output DP-2 --off \
    --output DP-3 --mode 1920x1080 --pos 1080x311 --rotate normal --primary \
    --output DP-4 --mode 1920x1080 --pos 3000x411 --rotate left \
    --output DP-5 --off
elif [[ "$host" = "REDL" ]]; then
    xrandr \
    --output eDP1 --mode 1920x1080 --primary
fi
