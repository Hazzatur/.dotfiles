# powerlevel10k {{{
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
# https://github.com/Aloxaf/fzf-tab/issues/176
export POWERLEVEL9K_PROMPT_CHAR_OVERWRITE_STATE=false
# }}}

# oh-my-zsh {{{
ZSH="/usr/share/oh-my-zsh/"

zstyle ':omz:update' mode disabled

source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

ZSH_CUSTOM=/home/hazzatur/.oh-my-zsh-custom

source /usr/share/zsh/plugins/fzf-tab-git/fzf-tab.plugin.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.plugin.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.plugin.zsh

plugins=(
  sudo
  dirhistory
)

fpath=("$ZSH_CUSTOM/completions" $fpath)

ZSH_CACHE_DIR=$HOME/.oh-my-zsh-custom/cache
if [[ ! -d $ZSH_CACHE_DIR ]]; then
  mkdir $ZSH_CACHE_DIR
fi

source $ZSH/oh-my-zsh.sh
# }}}

# bindings {{{
bindkey '^P' history-beginning-search-backward
bindkey '^N' history-beginning-search-forward

# zsh-autosuggestions
bindkey '^ ' autosuggest-execute # Bind ctrl + space to accept and execute current suggestion

if [[ $HOST = "RED" ]]; then
  bindkey '^[[1~' beginning-of-line
  bindkey '^[[4~' end-of-line
fi
# }}}

# export ~/.local/bin {{{
if [[ -d "$HOME/.local/bin" ]]; then
  export PATH=$HOME/.local/bin:$PATH
fi
# }}}

# restores alt + l lowercase word or ls (https://github.com/ohmyzsh/ohmyzsh/issues/5071) {{{
function _magic-alt-l () {
  if [[ -z "$BUFFER" ]]; then
    BUFFER="ls"
    zle accept-line
  else
    zle down-case-word
  fi
}
zle -N _magic-alt-l

bindkey '\el' _magic-alt-l
# }}}

# open projects menu {{{
function _menu-projects () {
  if [[ -z "$BUFFER" ]]; then
    export dir="$HOME/Personal"; "$HOME/.scripts/menu_projects" run_menu_projects dir "cd" "$TMUX_PANE"
  else
    export dir="$HOME/Personal"; "$HOME/.scripts/menu_projects" run_menu_projects dir
  fi
}
zle -N _menu-projects

bindkey '^[^F' _menu-projects
# }}}

# android {{{
export ANDROID_HOME=$HOME/Android/Sdk
if [[ -d "$ANDROID_HOME" ]]; then
  export PATH=$PATH:$ANDROID_HOME/emulator
  export PATH=$PATH:$ANDROID_HOME/tools
  export PATH=$PATH:$ANDROID_HOME/tools/bin
  export PATH=$PATH:$ANDROID_HOME/platform-tools
fi
# }}}

# conda {{{
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
# }}}

# flutter {{{
export FLUTTER_HOME="/opt/flutter"
if [[ -d "$FLUTTER_HOME" ]]; then
  export PATH="$PATH:$FLUTTER_HOME/bin"
fi
# }}}

# fzf {{{
source /usr/share/fzf/key-bindings.zsh
source /usr/share/fzf/completion.zsh
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS=" \
--color=bg+:#313244,bg:#1e1e2e,spinner:#f5e0dc,hl:#f38ba8 \
--color=fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc \
--color=marker:#f5e0dc,fg+:#cdd6f4,prompt:#cba6f7,hl+:#f38ba8"

# fzf-tab
zstyle ':fzf-tab:*' fzf-pad 4
zstyle ':fzf-tab:*' fzf-min-height 50
export LESSOPEN='|~/.scripts/lessfilter %s'

# disable sort when completing `git checkout`
zstyle ':completion:*:git-checkout:*' sort false
# set descriptions format to enable group support
zstyle ':completion:*:descriptions' format '[%d]'
# set list-colors to enable filename colorizing
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
# preview directory's content with eza when completing cd
zstyle ':fzf-tab:complete:(cd|-command-):*' fzf-preview 'less ${(Q)realpath}'
# switch group using `,` and `.`
zstyle ':fzf-tab:*' switch-group ',' '.'
# groups [full | brief | none]
zstyle ':fzf-tab:*' show-group full
# set prefix
zstyle ':fzf-tab:*' prefix ''

# give a preview of commandline arguments when completing `kill`
zstyle ':completion:*:*:*:*:processes' command "ps -u $USER -o pid,user,comm -w -w"
zstyle ':fzf-tab:complete:(kill|ps):argument-rest' fzf-preview \
  '[[ $group == "[process ID]" ]] && ps --pid=$word -o cmd --no-headers -w -w'
zstyle ':fzf-tab:complete:(kill|ps):argument-rest' fzf-flags --preview-window=down:3:wrap

# show systemd unit status
zstyle ':fzf-tab:complete:systemctl-*:*' fzf-preview 'SYSTEMD_COLORS=1 systemctl status $word'

# show file contents
zstyle ':fzf-tab:complete:*:*' fzf-preview 'less ${(Q)realpath}'

# environment variable
zstyle ':fzf-tab:complete:(-command-|-parameter-|-brace-parameter-|export|unset|expand):*' \
	fzf-preview 'echo ${(P)word}'

# git
zstyle ':fzf-tab:complete:git-(add|diff|restore):*' fzf-preview \
	'git diff $word | delta'
zstyle ':fzf-tab:complete:git-log:*' fzf-preview \
	'git log --color=always $word'
zstyle ':fzf-tab:complete:git-help:*' fzf-preview \
	'git help $word | bat -plman --color=always'
zstyle ':fzf-tab:complete:git-show:*' fzf-preview \
	'case "$group" in
	"commit tag") git show --color=always $word ;;
	*) git show --color=always $word | delta ;;
	esac'
zstyle ':fzf-tab:complete:git-checkout:*' fzf-preview \
	'case "$group" in
	"modified file") git diff $word | delta ;;
	"recent commit object name") git show --color=always $word | delta ;;
	*) git log --color=always $word ;;
	esac'

# brew
if [[ "$OSTYPE" == "darwin"* ]]; then
  which -s brew
  if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  else
    zstyle ':fzf-tab:complete:brew-(install|uninstall|search|info):*-argument-rest' fzf-preview 'brew info $word'
  fi
fi

function fzf-tab-tab() {
    if [[ $#BUFFER == 0 ]]; then
      BUFFER="cd "
      CURSOR=$#BUFFER
      fzf-tab-complete
    else
      fzf-tab-complete
    fi
}
zle -N fzf-tab-tab
bindkey '^I' fzf-tab-tab

function ctrl-d_complete_delete() {
  local char=${BUFFER[$CURSOR+1]}
  if [[ "$char" == " " || $CURSOR == ${#BUFFER} ]]; then
    BUFFER=${BUFFER:0:$CURSOR+1}
    CURSOR=$#BUFFER
    fzf-tab-complete
  else
    zle delete-char
  fi
}
zle -N ctrl-d_complete_delete
bindkey '^D' ctrl-d_complete_delete
# }}}

# google chrome {{{
if [[ -f "/usr/bin/google-chrome-stable" ]]; then
  export CHROME_EXECUTABLE=/usr/bin/google-chrome-stable
fi
# }}}

# navi {{{
if [[ -f "/usr/bin/navi" && "$TERM" != "screen-256color" ]]; then
  eval "$(navi widget zsh)"
fi
# }}}

# sudo {{{
if [[ -x "$(command -v /usr/bin/nvim)" ]]; then
  export SUDO_EDITOR='nvim'
  export EDITOR='nvim'
  export VISUAL='nvim'
fi
# }}}

# ssh {{{
if [ -z "$SSH_AUTH_SOCK" ] ; then
  export SSH_AUTH_SOCK=/run/user/$(id -u)/keyring/ssh
fi
# }}}

# volta {{{
export VOLTA_HOME="$HOME/.volta"
if [[ -d "$VOLTA_HOME" ]]; then
  export PATH="$VOLTA_HOME/bin:$PATH"
fi
# }}}

# browser {{{
export BROWSER="/usr/bin/vivaldi"
# }}}

# JetBrains scripts {{{
export PATH="$HOME/.local/share/JetBrains/Toolbox/scripts:$PATH"
# }}}

# ex: foldmethod=marker
