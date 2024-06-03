import os
import traceback
from rich import print
from time import sleep#perf_counter,
from platform import python_version
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
__version__ = '1.2.3'
__verdate__ = '2024-06-03 08:29'

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
    InstDict = {'mypy':False,'pipdeptree':False,'pylint':False,'pysftp':False,'pywmitool':False,'rich':False,'WMI':False}
#------------------------------------------------------------------------
    os.chdir(r'C:\Program Files\Python312\Scripts')
#----------------------------------------------------------------------- Установка, '-a'
    cmdlist = ['pipdeptree']
    UpdDict = {};Inst = False;Updt = False
    rez = cmdexec(cmdlist)
    restxt = rez.splitlines()#[2:]
    for ipr in restxt:
        if '==' in ipr:
            ai = ipr.split('==')[0]
            UpdDict[ai] = False #Создаем словарь установленных компонентов для обновления
            if ai in InstDict: InstDict[ai] = True #Помечаем ТРЕБУЕМЫЕ компоненты как установленные
    #----------------------------------------------------------------------------------------------
    for ii,ij in InstDict.items():
        if not ij:
            print(f'[cyan]{ii}')
            Inst = True
    if Inst:
        print('[cyan1]Необходимо установить перечисленные компоненты')
        if not input('Выполнить? :-> '):
            for ii,ij in InstDict.items():
                if not ij:
                    cmdlist = ['pip','install',f'{ii}']
                    cmdexecNoOut(cmdlist)
    print(f'\n[cyan]{'*'*100}\n')
    #-------------------------------------------------
    Upd2Dict = {}
    cmdlist = ['pip', 'list','-o']
    rez = cmdexec(cmdlist)
    if  rez:
        restxt = rez.splitlines()[2:]
        for ipr in restxt:
            tprg = ipr.split()[0]
            if tprg in UpdDict:
                UpdDict[tprg] = True #Помечаем компонентов требующие обновления
            else:Upd2Dict[tprg] = True #2-я очередь обновлений
    #------------------------------------------------------Обновление---------------------------------
    for ui,uj in UpdDict.items():
        if uj:
            print(f'[cyan]{ui}')
            Updt = True
    if Updt:
        print('[cyan1]Необходимо обновить указанные компоненты')
        if not input('Выполнить? :-> \n'):
            for ui,uj in UpdDict.items():
                if uj:
                    print(f'[cyan1]Модуль [cyan]{ui}')
                    cmdlist = ['pip','install','-U',f'{ui}']
                    cmdexecNoOut(cmdlist)
    if Upd2Dict:
        for ui,uj in Upd2Dict.items():
            if uj:
                print(f'[cyan1]Модуль [cyan]{ui}')
                cmdlist = ['pip','install','-U',f'{ui}']
                cmdexecNoOut(cmdlist)
    if not Updt and not Upd2Dict:
        print('Все модули последней версии')
    #----------------------------------------------------------------------
    input('\nВыход :-> ')
    os._exit(0)
