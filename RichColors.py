from rich import print
# from rich.console import Console
# cns = Console()
version = '1.0.3'
# Console.rule("[bold red]Chapter 2")
print('Образей цветной печати в терминале')
ListColors = (
    "bright_black",
    "white",
    "bright_white",
    "red",
    "orchid",
    # "bright_red",
    "yellow",
    "bright_yellow",
    "green",
    "green1",
    # "bright_green",
    "blue",
    "bright_blue",
    "cyan",
    "cyan1",
    # "bright_cyan",
    "magenta",
    # "bright_magenta",
    "purple"  )
for Colors in ListColors:
    if Colors:
        print (f'[{Colors}]{Colors = }')
    else:
        print()
#############################################################################
'Message',
'Warning',
'ErrPoSh',
'ErroCMD',
'Failure',
'Success',


