from libqtile import layout
from libqtile.config import Match

from .theme import theme

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": theme.sapphire,
    "border_normal": theme.background
}

layouts = [
    layout.Max(**layout_theme),
    layout.Columns(
        **layout_theme,
        border_focus_stack=[theme.mauve, theme.pink, theme.pink],
        border_on_single=True
    ),
    layout.TreeTab(
        font="MesloLGS NF",
        fontsize=10,
        bg_color=theme.background,
        active_bg=theme.sapphire,
        active_fg=theme.surface1,
        inactive_bg=theme.foreground,
        inactive_fg=theme.background,
        urgent_bg=theme.red,
        urgent_fg=theme.background,
        padding_x=0,
        padding_y=8,
        padding_left=0,
        section_bottom=16,
        section_top=16,
        section_left=16,
        section_fg=theme.pink,
        section_fontsize=10,
        vspace=3,
        panel_width=200,
        previous_on_rm=True,
        margin_left=8
    )
]

floating_layout = layout.Floating(
    border_focus=theme.sapphire,
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="dialog"),  # dialog boxes
        Match(wm_class="download"),  # downloads
        Match(wm_class="error"),  # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),  # kdenlive
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="notification"),  # notifications
        Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="toolbar"),  # toolbars
        Match(wm_class="Yad"),  # yad boxes
        Match(title="branchdialog"),  # gitk
        Match(title='Confirmation'),  # tastyworks exit box
        Match(title='Qalculate!'),  # qalculate-gtk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="tastycharts"),  # tastytrade pop-out charts
        Match(title="tastytrade"),  # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"),  # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"),  # tastytrade settings
        Match(wm_class="copyq"),  # copyq
        Match(wm_class="btop"),  # btop
        Match(wm_class="menu_personal"),  # Personal Menu
        Match(wm_class="menu_work")  # Work Menu
    ]
)
