import os
import traceback
from rich import print
# from threading import Thread
from time import perf_counter#,sleep
from platform import python_version
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
__version__ = '1.1.0'
__verdate__ = '2024-05-16 20:15'
gcmdres:str = ''

class DokExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)

###########################################################################################################################
def cmdexec(CMDcom:list)->str:
    # global
    cmdres = ''
    try:
    #---------------------------------------------------------------------------------------------------------------------
        with Popen(CMDcom, shell=True, stdout = PIPE, stderr = PIPE, encoding="cp866") as popps:
            pls = popps.communicate(timeout=60)
        if bool(pls[0]):cmdres = str(pls[0])
        if bool(pls[1]):raise DokExcept (pls[1])
    #----------------------------------------------------------------------------------------------------------------------
    except DokExcept as Mess:
        print(f'[yellow]Проблема:{Mess}')
    except TimeoutExpired as Mess:
        print(f'[yellow]Тиймаут:{Mess}')
    except Exception as MErs:
        print(f'[orchid]{MErs}')
        print(f'[orchid]{traceback.format_exc()}')
    return cmdres
###########################################################################################################################
if __name__ == '__main__':
    print(f'Обновление модулей Python ver: {python_version()}')
    start_time = tick_time_1 = tick_time_2 = perf_counter()

    os.chdir(r'C:\Program Files\Python312\Scripts')
    cmdlist = ['pip', 'list','-o']
    rez = cmdexec(cmdlist)
    # print(pls[1].decode('cp866'))
    if  rez:
        restxt = rez.splitlines()[2:]
        print(f'Доступны для обновления:2')
        for ipr in restxt:
            print(f'\t{ipr}')
        tick_time_1 = perf_counter()
        if not input('Обновить?:-> '):
            tick_time_2 = perf_counter()
            for it in restxt:
                print()
                tprg = it.split()[0]
                print(f'Модуль {tprg} версии {it.split()[1]}')
                cmdlist = ['pip','install','-U',f'{tprg}']
                # cmdexec(cmdlist)
    else:
        tick_time_2 = perf_counter()
        print('Все модули последней версии')
    #----------------------------------------------------------------------
    stop_time = perf_counter()
    Inetrval_1 = tick_time_1 - start_time
    Inetrval_2 = stop_time - tick_time_2
    input(f'\n{Inetrval_1:.>5} : {Inetrval_2:.>5} :-> ')
    os._exit(0)
