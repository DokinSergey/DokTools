import os
from rich import print
# from rich.console import Console
# cns = Console()
version = '1.0.3'
# Console.rule("[bold red]Chapter 2")
ColorFile = 'RichColors88.txt'
print('Образей цветной печати в терминале')
#################################################################################
rbg = 90
for ib in range(0,256,25):# (0,15,20,30,35,45,90,110):
    for ig in range(0,256,25):# (0,15,20,30,35,45,90,110):
        for ir in range(0,256,25):#(0,15,20,30,35,45,90,110,115,135,150,155,175,180,190,205,235,245,256):
            if (ir + ig) < rbg or (ig + ib) < rbg or (ir + ib) < rbg:continue
            print (f'[rgb({ir},{ig},{ib})]Colors ={ir:3},{ig:3},{ib:3}')


#############################################################################
input('Выход:-> ')
os._exit(0)
