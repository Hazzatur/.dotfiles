#!/bin/bash

sudo curl -o /etc/X11/edid.bin --create-dirs "https://raw.githubusercontent.com/Hazzatur/Notes/main/edid.bin"
sudo nvidia-xconfig --custom-edid="GPU-0.DP-4:/etc/X11/edid.bin"
