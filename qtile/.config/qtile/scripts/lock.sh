#!/bin/bash

pgrep -x i3lock && exit

alpha='dd'
background='#11111b'
selection='#1e1e2e'
comment='#b4befe'

yellow='#f9e2af'
orange='#fab387'
red='#f38ba8'
magenta='#f5c2e7'
blue='#89b4fa'
cyan='#89dceb'
green='a6e3a1'

i3lock \
  --insidever-color=$selection$alpha \
  --insidewrong-color=$selection$alpha \
  --inside-color=$selection$alpha \
  --ringver-color=$green$alpha \
  --ringwrong-color=$red$alpha \
  --ringver-color=$green$alpha \
  --ringwrong-color=$red$alpha \
  --ring-color=$blue$alpha \
  --line-uses-ring \
  --keyhl-color=$magenta$alpha \
  --bshl-color=$orange$alpha \
  --separator-color=$selection$alpha \
  --verif-color=$green \
  --wrong-color=$red \
  --layout-color=$blue \
  --date-color=$blue \
  --time-color=$blue \
  --screen 1 \
  --blur 1 \
  --clock \
  --indicator \
  --time-str="%I:%M %p" \
  --date-str="%B, %A %e %Y" \
  --verif-text="Checking..." \
  --wrong-text="Wrong pass" \
  --noinput="No Input" \
  --lock-text="Locking..." \
  --lockfailed="Lock Failed" \
  --radius=120 \
  --ring-width=10 \
  --pass-media-keys \
  --pass-screen-keys \
  --pass-volume-keys \
  --time-font="MesloLGS NF" \
  --date-font="MesloLGS NF" \
  --layout-font="MesloLGS NF" \
  --verif-font="MesloLGS NF" \
  --wrong-font="MesloLGS NF"
