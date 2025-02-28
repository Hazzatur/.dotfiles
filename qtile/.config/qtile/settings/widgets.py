from .CatppuccinMocha import CatppuccinMocha

colors = CatppuccinMocha()

widget_defaults = dict(
    font="MesloLGS NF",
    fontsize=12,
    padding=0,
    background=colors.background
)

extension_defaults = widget_defaults.copy()
