import os
# from rich import print
version = '1.0.3'
print('Образей цветной печати в терминале')

#--------------------------------------------------------------------------
# for Colors in ListColors:
    # if Colors:
        # print (Colors + f'\tColors = {Colors = }')
    # else:
        # print()
for ii in range(127):
    icolors = f'\033[{ii}m'
    print (f'{icolors}Colors = {icolors = }')
#############################################################################
input('Выход:-> ')
os._exit(0)
