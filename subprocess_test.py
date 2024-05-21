import os
import traceback
# from rich import print
from time import perf_counter,sleep
from subprocess import Popen,TimeoutExpired#,SubprocessError, PIPE
__version__ = '1.1.3'
__verdate__ = '2024-05-17 11:43'

###########################################################################################################################
def cmdexecNoOut(CMDcom:list):
    try:
    #---------------------------------------------------------------------------------------------------------------------,stdout = PIPE,stderr = PIPE
        Popen(CMDcom, shell=True, encoding="cp866")
    #----------------------------------------------------------------------------------------------------------------------
    except TimeoutExpired as Mess:
        print(f'[yellow]Тиймаут:{Mess}')
    except Exception as MErs:
        print(f'[orchid]{MErs}')
        print(f'[orchid]{traceback.format_exc()}')
###########################################################################################################################
if __name__ == '__main__':
    print(f'Тестирование модуля сопроцесса: {__version__}')
    start_time = perf_counter()
    for ai in range(10):
        cmdlist = ['timeout','/t','20','/nobreak']# >nul
           try:
        #---------------------------------------------------------------------------------------------------------------------,stdout = PIPE,stderr = PIPE
                Popen(CMDcom, shell=True, encoding="cp866")
        #----------------------------------------------------------------------------------------------------------------------
    except TimeoutExpired as Mess:
        print(f'[yellow]Тиймаут:{Mess}')
    except Exception as MErs:
        print(f'[orchid]{MErs}')
        print(f'[orchid]{traceback.format_exc()}')
        
        
        
        cmdexecNoOut(cmdlist)
        sleep(0.1)
        print()
        sleep(0.9)
    sleep(1)
    print()
    sleep(1)
    #----------------------------------------------------------------------
    stop_time = perf_counter()
    Inetrval = stop_time - start_time
    input(f'\n{Inetrval:.5f} :-> ')
    # os._exit(0)
