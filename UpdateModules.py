import os
import traceback
from rich import print
from time import perf_counter,sleep
from platform import python_version
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
__version__ = '1.1.5'
__verdate__ = '2024-05-30 10:1143'

class DokExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)

###########################################################################################################################
def cmdexec(CMDcom:list)->str:
    # global
    cmdres = ''
    try:
    #---------------------------------------------------------------------------------------------------------------------
        print('[', end = '', flush=True)
        with Popen(CMDcom, shell=True,stdout = PIPE,stderr = PIPE, encoding="cp866") as popps:
            for ici in range(100):
                if popps.poll():break
                if not ici % 10:print('[green]#', end = '', flush=True)
                sleep(0.1)
            print(f'] {(ici+1)/10:.2f} c')
            pls = popps.communicate()
        # print(f'Результат:{pls}')
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
def cmdexecNoOut(CMDcom:list)->str:
    try:
    #---------------------------------------------------------------------------------------------------------------------,stdout = PIPE,stderr = PIPE
        with Popen(CMDcom, shell=True, encoding="cp866") as popps:
            popps.communicate(120)
    #----------------------------------------------------------------------------------------------------------------------
    except TimeoutExpired as Mess:
        print(f'[yellow]Тиймаут:{Mess}')
    except Exception as MErs:
        print(f'[orchid]{MErs}')
        print(f'[orchid]{traceback.format_exc()}')
###########################################################################################################################
if __name__ == '__main__':
    print(f'Обновление модулей вер.{__version__} для Python ver.{python_version()}')
    start_time = tick_time_1 = tick_time_2 = perf_counter()
#------------------------------------------------------------------------
    os.chdir(r'C:\Program Files\Python312\Scripts')
    cmdlist = ['pip', 'list','-o']
    rez = cmdexec(cmdlist)
    # print(pls[1].decode('cp866'))
    if  rez:
        restxt = rez.splitlines()[2:]
        print(f'[cyan1]Доступны для обновления:{len(restxt)}')
        for ipr in restxt:
            print(f'\t[cyan]{ipr}')
        tick_time_1 = perf_counter()
        if not input('Обновить?:-> '):
            tick_time_2 = perf_counter()
            for it in restxt:
                print()
                tprg = it.split()[0]
                print(f'[cyan1]Модуль [cyan]{tprg} [cyan1]версии [cyan]{it.split()[1]}')
                cmdlist = ['pip','install','-U',f'{tprg}']
                # cmdlist = ['timeout','/t','5','/nobreak']# >nul
                cmdexecNoOut(cmdlist)
    else:
        tick_time_2 = perf_counter()
        print('Все модули последней версии')
    #----------------------------------------------------------------------
    stop_time = perf_counter()
    Inetrval_1 = tick_time_1 - start_time
    Inetrval_2 = stop_time - tick_time_2
    input(f'\n{Inetrval_1:.5f} : {Inetrval_2:.5f} :-> ')
    os._exit(0)
