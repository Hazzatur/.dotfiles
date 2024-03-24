local wezterm = require 'wezterm'
local act = wezterm.action
local config = wezterm.config_builder()

config.color_scheme = 'Catppuccin Mocha'
config.default_cursor_style = 'BlinkingBlock'
config.default_prog = { '/usr/bin/zsh', '-c', 'tmux', 'new', '-As0' }
config.font = wezterm.font 'MesloLGS NF'
config.font_size = 10.0
config.hide_mouse_cursor_when_typing = true
config.mouse_bindings = {
    {
        event = { Down = { streak = 1, button = 'Right' } },
        mods = 'CTRL',
        action = act.PasteFrom("PrimarySelection")
    }
}
config.term = 'wezterm'
config.window_background_opacity = 0.9

return config
