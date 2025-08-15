import os
from rich import print
# from rich.console import Console
# cns = Console()
version = '1.0.3'
# Console.rule("[bold red]Chapter 2")
ColorFile = 'RichColors88.txt'
print('Образей цветной печати в терминале')
if os.path.isfile(ColorFile):
    with open(ColorFile, mode='r', encoding='utf_8') as coltxt:
        ListColors = coltxt.readlines()
else:
    ListColors = (
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
        )
#--------------------------------------------------------------------------
for Clrs in ListColors:
    Colors = Clrs.strip()
    if Colors:
        print (f'[{Colors}]{Colors = }')
    else:
        print()

#############################################################################
input('Выход:-> ')
os._exit(0)
