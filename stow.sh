#!/bin/bash

echo "Setting up dotfiles..."
echo "Initializing submodules..."
git submodule update --init

# -----------------------------------------
echo "Creating directories..."
mkdir -p ~/.config/{btop,copyq/themes,dunst,gtk-3.0,flameshot,kitty,Kvantum,picom,qBittorrent/themes,qtile,qt5ct,qt6ct,rofi,Thunar,xournalpp/templates,yazi/themes}
mkdir -p ~/.gitkraken/themes
mkdir -p ~/.local/share/applications
mkdir -p ~/.screenlayout
mkdir -p ~/.scripts
mkdir -p ~/.setup
mkdir -p ~/.ssh
mkdir -p ~/.tmux_custom
mkdir -p ~/.wallpaper
mkdir -p ~/Pictures/Screenshots

# -----------------------------------------
echo "Downloading zsh completions..."
export ZSH_CUSTOM="$HOME/.oh-my-zsh-custom"
mkdir -p "$ZSH_CUSTOM"/{completions,plugins,themes,cache}

_completions=(
  "https://raw.githubusercontent.com/tjquillan/zsh-windscribe-completions/master/_windscribe"
  "https://cheat.sh/:zsh"
  "https://raw.githubusercontent.com/conda-incubator/conda-zsh-completion/master/_conda"
  "https://github.com/sharkdp/fd/blob/master/contrib/completion/_fd"
)

for completion in "${_completions[@]}"; do
  if [[ ! -f "$ZSH_CUSTOM/completions/${completion##*/}" ]]; then
    curl -sSL "$completion" -o "$ZSH_CUSTOM/completions/${completion##*/}"
    if [[ "${completion##*/}" == ":zsh" ]]; then
      mv "$ZSH_CUSTOM/completions/:zsh" "$ZSH_CUSTOM/completions/_cht"
    fi
  fi
done

if [[ ! -f "$ZSH_CUSTOM/completions/_volta" ]]; then
  volta completions zsh > "$ZSH_CUSTOM/completions/_volta"
fi

# -----------------------------------------
echo "Stowing directories..."
for directory in */ ; do
    stow --target="$HOME" "$directory" --restow
done
