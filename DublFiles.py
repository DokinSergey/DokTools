import os
__version__ = '1.0.1'
__verdate__ = "2023-12-02 17:37"

startpath = 'F:\\'
extfiles = '.pdf'
lb = {}
dubl = {}
ca = 0; cb = 0
try:
# просто перебираем файлы, сравнивая их расширение
    for a,_,b in os.walk(startpath):
        if b:
            for bn in b:
                if bn.endswith(extfiles):
                    if  bn not in lb:
                        lb[bn] = a
                        # print(f'\t{bn = 76}')
                        ca += 1
                    else:
                        dubl[bn] = a
                        cb += 1
except Exception as DErr:
    print(str(DErr))
finally:
    for ik, iv in dubl.items():
        print(f'  {ik}')
        print(f'\t{iv}')
        print(f'\t{lb[ik]}')
        print('-' *70)
    print(ca,cb)
