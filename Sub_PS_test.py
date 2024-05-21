import os
import traceback
from rich import print
from time import perf_counter,sleep
from platform import python_version
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
__version__ = '1.1.3'
__verdate__ = '2024-05-17 11:43'

class DokExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)

###########################################################################################################################
def cmdexec(ps_str:str)->dict:
    # global
    cmdres = {}
    try:
    #---------------------------------------------------------------------------------------------------------------------
        ici = 0#, stdout = PIPE, encoding="cp866"
        print('[', end = '', flush=True)
        start_t = perf_counter()
        with Popen(['powershell', ps_str], stdout = PIPE,stderr = PIPE) as popps:
        # popps = Popen(['powershell', ps_str], stdout = PIPE,stderr = PIPE)
            # while popps.poll() is None:
                # if ici and not ici % 500:print('[green]#', end = '')
                # print(f'[green] {popps.poll()}', end = ''), flush=True
                # sleep(0.1)
                # ici += 1
            # print(f'] {(ici+1)/100:.2f} c')
            # print(f'Результат:{popps.poll()}')
            pls = popps.communicate(1)
        # while popps.poll() is None:
                # astr = popps.stdout.readline().decode('cp866')
        stop_t = perf_counter()
        Intrvl = stop_t - start_t
        print(f'Результат:{popps.poll()} за время {Intrvl:.5f}')
        # if bool(pls[1]):raise DokExcept (pls[1])
        if bool(pls[0]):
            for astr in pls[0].decode('cp866').splitlines():
                # rf = [];namefile = ''
                if astr and astr[:5] not in ('Mode ','---- ','    К'):
                    # print(astr)#.split()
                    nfl = astr[50:].strip()
                    dfl = astr[14:25]
                    tfl = astr[29:35]
                    lfl = (astr[35:50].strip())
                    print(nfl,dfl,tfl,lfl)
                    # cmdres[namefile] = rf
                    # irr = istr.split()
                    # cmdres.append([irr[0],irr[1],irr[2],irr[3]])

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
    print(f'Тест PowerShell in Subprocess Python ver: {python_version()}')
    start_time = tick_time_1 = tick_time_2 = perf_counter()
    #----------------------------------------------------------------------
    ResFile = fr'{os.path.realpath('')}\res.txt'
    # -Recurse
    # psstr = r'Get-ChildItem -Path D:\ -File | FT Name, LastWriteTime -AutoSize -HideTableHeaders'\Квартира Ogromnov\
    # | FT LastWriteTime,Length,Name -AutoSize -HideTableHeaders
    # psstr = fr'Get-ChildItem -Path D:\Photo\Ogromnov\ -File | Out-File -FilePath {ResFile} -Width 200 -Force'
    psstr = fr'Get-ChildItem -Path D:\Photo\Ogromnov -File | out-string -Width 200'
    rr = cmdexec(psstr)
    print(rr)
    #----------------------------------------------------------------------
    stop_time = perf_counter()
    Inetrval = stop_time - start_time
    input(f'\n{Inetrval:.5f}  :-> ')
    os._exit(0)
