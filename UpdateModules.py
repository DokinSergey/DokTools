import os,traceback,platform
from rich import print as rpn
from time import sleep#perf_counter,
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
from datetime import datetime,timezone,date,timedelta
#####################################################################################################################################################
_author  = 't.me/dokin_sergey'
_version = '1.3.3'
_verdate = '2024-06-06 21:39'
_LogLocPath = os.path.realpath('')
_GlobaLen = 120
class DokExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)
debug = False
InstDict = {'setuptools':False,'pylint':False,'mypy':False,'pipdeptree':False,'pysftp':False,'pywmitool':False,'rich':False,'WMI':False}
#####################################################################################################################################################
try:
    _LogFile  = fr'{_LogLocPath}\UpdMod_logg_{str(date.today())}.txt'
    _InstFile = fr'{_LogLocPath}\UpdMod_inst_{str(date.today())}.txt'
    _UpdFile  = fr'{_LogLocPath}\UpdMod_updt_{str(date.today())}.txt'
except Exception as EMess:
    rpn(f'[orchid]Ошибка: [yellow]{EMess}')
    rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
#####################################################################################################################################################
def WordRead(Wrd:str)->bool:
    Wres = False
    if   Wrd.isalnum():
        Wres = True
    else:
        for iw in Wrd:
            if (ord(iw) in range(33,125)) or (ord(iw) in range(192,255)):
                Wres = True
                break
    return Wres
################################################################################################################################################################
def FileWrite(FlName:str,NetStr:str,WMess:tuple[str,...])->bool:# = '',LMess:tuple[str] = ())->bool:
    try:
        with open(FlName, mode = 'a', encoding = 'utf_8') as fwl:
            for istr in WMess:
                print(f'{NetStr}{istr}', file = fwl)
    except Exception as FMess:
        LogErrDebug('Failure',f'{FMess}','FileWrite')
        LogErrDebug('Failure',f'{traceback.format_exc()}','FileWrite')
        rpn(f'[orchid]Ошибка: [yellow]{FMess}')
        rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
        return False
    return True
################################################################################################################################################################
def LogErrDebug(Mess1:str,Mess2:str, Mess3:str = '')->bool:
    TypeMess = ('Warning','Failure','Update_','Install','Message','ErroCMD')#Caution
    if len(Mess1) == 7 and Mess1 in TypeMess:
        TMess = Mess1#+' '
        RMess = Mess2
        Funct = Mess3
    else:
        TMess = 'Message'
        RMess = Mess1
        Funct = Mess2
    ListMess = []
    try:
        dtnow = datetime.now(timezone.utc) + timedelta(hours=3)
        dtstr = dtnow.strftime("%H:%M:%S")
        PrnStr = f'{dtstr};{TMess};'
        lFN = 12
        FN = f'{Funct:{lFN}} ;' if Funct else f'{" ":{lFN}} ; '
        PrnStr += FN
        ListStr = str(RMess).splitlines()
        tstr = ''
        for iStr in ListStr:
            if iStr and not iStr.isspace():
                ListWr = iStr.split()
                for iLW in ListWr:
                    if iLW:# and WordRead(iLW):
                        tstr += f' {iLW}'
                    if len(tstr) >_GlobaLen+1:
                        ListMess.append(tstr)
                        tstr = ''
        if tstr: ListMess.append(tstr)
    #---------------------------------------------------------------------------------------------------------------------------
        TupleMess = tuple(ListMess)
        if _LogFile:
            if TMess not in ('Install','Update_'):FileWrite(_LogFile,PrnStr,TupleMess)
            if TMess == 'Install':FileWrite(_LogFile,PrnStr,(f'{RMess}',))
            if TMess == 'Update_':FileWrite(_LogFile,PrnStr,(f'{RMess}',))
        #------------------------------------------------------------------------------------------------
        if debug: rpn(f'{dtstr} ; [yellow]{RMess}')
    except Exception as Err:
        Led = False
        if debug:rpn(str(Err))
    else:
        Led = True
    return Led
#####################################################################################################################################################
def cmdexec(CMDcom:list[str])->str:
    # global
    cmdres = ''
    try:
    #---------------------------------------------------------------------------------------------------------------------
        rpn('[', end = '', flush=True)
        with Popen(CMDcom, shell=True,stdout = PIPE,stderr = PIPE, encoding="cp866") as popps:
            for ici in range(100):
                if popps.poll():break
                if not ici % 5:rpn('[green]#', end = '', flush=True)
                sleep(0.1)
            rpn(f'] {(ici+1)/10:.2f} c')
            pls = popps.communicate()
        # rpn(f'Результат:{pls}')
        if bool(pls[0]):cmdres = str(pls[0])
        if bool(pls[1]):raise DokExcept (pls[1])
    #----------------------------------------------------------------------------------------------------------------------
    except DokExcept as Mess:
        rpn(f'[yellow]Проблема:{Mess}')
        LogErrDebug('Warning',f'Проблема:{Mess}','cmdexec')
    except TimeoutExpired as Mess:
        LogErrDebug('Failure',f'Таймаут:{Mess}','cmdexec')
        rpn(f'[yellow]Таймаут:{Mess}')
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexec')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexec')
        rpn(f'[orchid]{MErs}')
        rpn(f'[orchid]{traceback.format_exc()}')
    return cmdres
###########################################################################################################################
def cmdexecNoOut(CMDcom:list[str])->None:
    try:
    #---------------------------------------------------------------------------------------------------------------------,stdout = PIPE,stderr = PIPE
        with Popen(CMDcom, shell=True, encoding="cp866") as popps:
            popps.communicate(timeout=120)
    #----------------------------------------------------------------------------------------------------------------------
    except TimeoutExpired as Mess:
        rpn(f'[yellow]Тиймаут:{Mess}')
        LogErrDebug('Failure',f'Таймаут:{Mess}','cmdexecNoOut')
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexecNoOut')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexecNoOut')
        rpn(f'[orchid]{MErs}')
        rpn(f'[orchid]{traceback.format_exc()}')
###########################################################################################################################
if __name__ == '__main__':
    rpn(f'Обновление модулей вер.{_version} для Python ver.{platform.python_version()}')
    debug = True
    #---------------------------------------------------------------------------------------------------------------------------
    FileWrite(_LogFile,'',('*'*(_GlobaLen+20),))
    if os.path.isfile(_InstFile):FileWrite(_InstFile,'',('*'*(_GlobaLen+20),))
    if os.path.isfile(_UpdFile):FileWrite(_UpdFile,'',('*'*(_GlobaLen+20),))
    #--------------------------------------------------------------------------------------------------------------------------------------
    LogErrDebug('Message',f'Программы установки и обновления Pytnob: {_version} ; от {_verdate} ; Автор {_author} ; ', os.path.basename(__file__))
    LogErrDebug('Message',f'Установлен Python ver.{platform.python_version()} ; {platform.python_build()[1]} ; {platform.python_compiler()}', os.path.basename(__file__))
#------------------------------------------------------------------------
    os.chdir(r'C:\Program Files\Python312\Scripts')
#----------------------------------------------------------------------- Установка, '-a'
    cmdlist = ['pipdeptree',]
    UpdDict = {};Inst = False;Updt = False
    rez = cmdexec(cmdlist)
    restxt = rez.splitlines()#[2:]
    if restxt:LogErrDebug('Install','Установлены модули ; версий', os.path.basename(__file__))
    for ipr in restxt:
        if '==' in ipr:
            ai,bi = ipr.split('==')
            LogErrDebug('Install',f'{ai:18} ; {bi}', os.path.basename(__file__))
            UpdDict[ai] = False #Создаем словарь установленных компонентов для обновления
            if ai in InstDict: InstDict[ai] = True #Помечаем ТРЕБУЕМЫЕ компоненты как установленные
    #----------------------------------------------------------------------------------------------
    for ii,ij in InstDict.items():
        if not ij:
            rpn(f'[cyan]{ii}')
            Inst = True
    if Inst:
        rpn('[cyan1]Необходимо установить перечисленные компоненты')
        if not input('Выполнить? :-> '):
            LogErrDebug('Install','Дополнительно установлены', os.path.basename(__file__))
            for ii,ij in InstDict.items():
                if not ij:
                    cmdlist = ['pip','install',f'{ii}']
                    cmdexecNoOut(cmdlist)
                    LogErrDebug('Install',f'{ii:20} ', os.path.basename(__file__))
    rpn(f'\n[cyan]{'*'*100}\n')
    #-------------------------------------------------
    Upd2Dict = {}
    cmdlist = ['pip', 'list','-o']
    rez = cmdexec(cmdlist)
    if  rez:
        restxt = rez.splitlines()[2:]
        if restxt:LogErrDebug('Install','Необходимо обновить указанные компоненты', os.path.basename(__file__))
        for ipr in restxt:
            name,old,new,_ = ipr.split()#[0]
            LogErrDebug('Install',f'{name:18} ; {old:8} ; {new:8}', os.path.basename(__file__))
            if name in UpdDict:
                UpdDict[name] = True #Помечаем компонентов требующие обновления
            else:Upd2Dict[name] = True #2-я очередь обновлений
    #------------------------------------------------------Обновление---------------------------------
    for ui,uj in UpdDict.items():
        if uj:
            rpn(f'[cyan]{ui}')
            Updt = True
    if Updt:
        rpn('[cyan1]Необходимо обновить указанные компоненты')
        if not input('Выполнить? :-> \n'):
            LogErrDebug('Install','Обновленные модули', os.path.basename(__file__))
            for ui,uj in UpdDict.items():
                if uj:
                    rpn(f'[cyan1]Модуль [cyan]{ui}')
                    cmdlist = ['pip','install','-U',f'{ui}']
                    cmdexecNoOut(cmdlist)
                    LogErrDebug('Install',f'{ui:20} ', os.path.basename(__file__))
    if Upd2Dict:
        for ui,uj in Upd2Dict.items():
            if uj:
                rpn(f'[cyan1]Модуль [cyan]{ui}')
                cmdlist = ['pip','install','-U',f'{ui}']
                cmdexecNoOut(cmdlist)
                LogErrDebug('Install',f'{ui:20} ', os.path.basename(__file__))
    if not Updt and not Upd2Dict:
        rpn('Все модули последней версии')
    #----------------------------------------------------------------------
    input('\nВыход :-> ')
    os._exit(0)
