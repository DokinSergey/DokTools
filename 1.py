import os,traceback
from rich import print as rpn
try:
    NameFiler = 'RichColorsR.txt'
    NameFilew = 'RichColors.txt'
    with open(NameFiler, mode='r', encoding='utf_8') as txt1:
        listtxt = txt1.readlines()
    #------------------------------------------------------------
    tres = ''
    with open(NameFilew, mode='w', encoding='utf_8') as txt2:
        for tstr in listtxt:
            tcol = tstr.split('"')
            tres += f"'{tcol[1]}',"
            print(tcol[1],file=txt2)
    rpn(tres)
except Exception as MErs:
    rpn(f'[orchid]{MErs}')
    rpn(f'[orchid]{traceback.format_exc()}')
input('\nВыход :-> ')
os._exit(0)
