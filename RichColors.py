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
        "bright_red",
        "red1",
        "yellow",
        "bright_yellow",
        "khaki1",
        "green",
        "bright_green",
        "green1",#
        "honeydew2",
        "blue",
        "bright_blue",
        "blue1",
        "cyan",
        "cyan1",#
        "bright_cyan",
        "light_cyan1",
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
