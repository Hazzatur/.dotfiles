git submodule update --init

mkdir -p ~/.config/{alacritty,btop,copyq,gtk-3.0,picom,qBittorrent,qtile,ranger,rofi}
mkdir -p ~/.scripts
mkdir -p ~/.screenlayout
mkdir -p ~/.ssh
mkdir -p ~/.tmux_custom
mkdir -p ~/.wallpaper
mkdir -p ~/.oh-my-zsh-custom

for directory in */ ; do
    stow --target=$HOME $directory --restow
done
