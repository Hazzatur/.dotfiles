#!/bin/bash

home_dir=$1
wallpaper=$2

sudo mkdir -p /usr/share/backgrounds
sudo cp "$wallpaper" /usr/share/backgrounds/custom.jpg
sudo cp "$home_dir"/.setup/slick-greeter.conf /etc/lightdm/slick-greeter.conf
sudo sed -i 's,#greeter-session=.*,greeter-session=lightdm-slick-greeter,g' /etc/lightdm/lightdm.conf
sudo sed -i "s,#display-setup-script=.*,display-setup-script=$home_dir/.screenlayout/monitor.sh,g" /etc/lightdm/lightdm.conf
sudo chsh -s /usr/bin/zsh root
sudo chsh -s /usr/bin/zsh "$USER"
sudo ln -s /lib/libncursesw.so.6 /lib/libncurses.so.5
sudo ln -s /lib/libtinfo.so.6 /lib/libtinfo.so.5
papirus-folders -C cat-mocha-sapphire --theme Papirus-Dark
printf "[UiSettings]\nColorScheme=KvArcDark" > "$home_dir"/.config/okularrc
sed -i "s,savePath=.*,savePath=$home_dir/Pictures/Screenshots,g" "$home_dir"/Personal/.dotfiles/flameshot/.config/flameshot/flameshot.ini
sudo usermod -aG docker "$USER"
sudo systemctl enable --now docker.service
sudo systemctl enable --now containerd.service
sudo systemctl enable --now bluetooth.service
rustup default stable
volta install node@latest
sudo systemctl enable --now lightdm.service
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
