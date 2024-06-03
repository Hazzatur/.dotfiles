#!/bin/bash

if [ "$1" == "up" ]; then
    brightnessctl s 5%+ && notify-send -t 1000 "Brightness - $(brightnessctl -d intel_backlight g | awk -F, '{print $1/96000*100}' | tr -d %)%"
elif [ "$1" == "down" ]; then
    brightnessctl s 5%- && notify-send -t 1000 "Brightness - $(brightnessctl -d intel_backlight g | awk -F, '{print $1/96000*100}' | tr -d %)%"
else
    echo "Usage: $0 {up|down}"
    exit 1
fi
