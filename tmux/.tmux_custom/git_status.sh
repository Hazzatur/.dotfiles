show_git_status() {
    local index=$1
    local icon=$(get_tmux_option "@catppuccin_git_status_icon" "")
    local color=$(get_tmux_option "@catppuccin_git_status_color" "$thm_blue")
    local path=$(tmux display-message -p "#{pane_current_path}")
    local text="$(get_tmux_option "@catppuccin_test_text" "#($HOME/.tmux_custom/dracula_git.sh)")"

    local module=$(build_status_module "$index" "$icon" "$color" "$text")
    echo "$module"
}
