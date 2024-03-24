git submodule update --init

mkdir -p ~/.config/{btop,copyq/themes,gtk-3.0,picom,qBittorrent/themes,qtile,ranger,rofi,wezterm}
mkdir -p ~/.gitkraken/themes
mkdir -p ~/.screenlayout
mkdir -p ~/.scripts
mkdir -p ~/.ssh
mkdir -p ~/.tmux_custom
mkdir -p ~/.wallpaper
mkdir -p ~/.oh-my-zsh-custom/{cache,completions}

for directory in */ ; do
    stow --target="$HOME" "$directory" --restow
done
