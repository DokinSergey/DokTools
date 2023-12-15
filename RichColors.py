from rich import print
print('Образей цветной печати в терминале')
ListColors = (
    "white",
    "bright_white",
    "bright_black",
    "red",
    "bright_red",
    "yellow",
    "bright_yellow",
    "green",
    "bright_green",
    "bright_blue",
    "blue",
    "magenta",
    "bright_magenta",
    "purple"  )
for Colors in ListColors:
    if Colors:
        print (f'[{Colors}]{Colors = }')
    else:
        print()
