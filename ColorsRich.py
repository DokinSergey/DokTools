import os
from rich import print as rpn
# nuitka-project: --mode=standalone
# nuitka-project: --windows-console-mode=attach
#force
# nuitka-project: --windows-icon-from-ico=ColorsRich.png
# nuitka-project: --include-package=rich
# nuitka-project: --company-name='t.me/dokin_sergey'
# nuitka-project: --product-name='Rich color printing'
# nuitka-project: --file-version=1.0.3
# nuitka-project: --product-version=1.0.3

version = '1.0.3'

rpn('Образей цветной печати в терминале')
ListColors = [
    "bright_black",
    "white",
    "bright_white",
    "red",
    "red1",
    "bright_red",
    "orange_red1",
    "dark_orange",
    "orange1",
    "yellow1",
    "khaki1",
    "green_yellow",
    "light_green",
    "green1",
    "spring_green3",
    "dark_cyan",
    "cyan3",
    "bright_cyan",
    "cyan1",
    "turquoise2",
    "deep_sky_blue1",
    "dodger_blue3",
    "magenta",
    "orchid",
    "purple", #
    "violet",
    "magenta1",
    ]
#--------------------------------------------------------------------------
for Clrs in ListColors:
    Colors = Clrs.strip()
    if Colors:
        rpn(f'[{Colors}]{Colors = }')
    else:
        rpn()

#############################################################################
input('Выход:-> ')
os._exit(0)
