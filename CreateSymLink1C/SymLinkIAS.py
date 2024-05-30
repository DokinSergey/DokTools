import os
import traceback
from wmi import WMI
from rich import print as rpn
from datetime import datetime,timezone,date,timedelta
#--------------------------------
_AUTHOR  = 't.me/dokin_sergey'
_VERSION = '1.0.7 IAS'
_VERDATE = '2024-05-30 12:48'
#---------------------------------------------
ibapath = r'\\moscow\ibases'
# SRKpath = r'\\more\COPY\_log\psql-dump-enabled'
debug = False
_LogNetPath = r'\\more\copy\_log\MakeSymLink'
_LogLocPath = os.path.realpath('')
_USERNAME= os.getlogin()
_GlobaLen = 140
################################################################################################################################################################
try:
    if not os.path.isdir(_LogNetPath):os.makedirs(_LogNetPath,exist_ok=True)
    LogFile =  fr'{_LogNetPath}\{str(date.today())}_log_ias.txt'
    ErrFile =  fr'{_LogNetPath}\{str(date.today())}_err_ias.txt'
    ResFile =  fr'{_LogNetPath}\{str(date.today())}_res_ias.txt'
    _LogFile = fr'{_LogLocPath}\{str(date.today())}_log_ias.txt'
    _ErrFile = fr'{_LogLocPath}\{str(date.today())}_err_ias.txt'
    _ResFile = fr'{_LogLocPath}\{str(date.today())}_res_ias.txt'
except Exception as Mess:
    rpn(f'[orchid]Ошибка: [yellow]{Mess}')
    rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
################################################################################################################################################################
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
def FileWrite(FlName:str,WMess:tuple[str,...])->bool:# = '',LMess:tuple[str] = ())->bool:
    try:
        with open(FlName, mode = 'a', encoding = 'utf_8') as fwl:
            for istr in WMess:
                print(f'{istr}', file = fwl)
    except Exception as FMess:
        rpn(f'[orchid]Ошибка: [yellow]{FMess}')
        rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
        return False
    return True
################################################################################################################################################################
def LogErrDebug(Mess1:str,Mess2:str, Mess3:str = '')->bool:
    TypeMess = ('Warning','Failure','Success','ErrPoSh','Message','ErroCMD')#Caution
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
        PrnStr = f'{dtstr};{_USERNAME:12};{TMess};'
        lFN = 12
        FN = f'{Funct:{lFN}} ;' if Funct else f'{" ":{lFN}} ;'
        PrnStr += FN
        ListStr = str(RMess).splitlines()
        tstr = ''
        for iStr in ListStr:
            if iStr and not iStr.isspace():
                ListWr = iStr.split()
                for iLW in ListWr:
                    if iLW and WordRead(iLW):
                        tstr += f' {iLW}'
                    if len(tstr) >_GlobaLen:
                        # print(tstr)
                        ListMess.append(tstr)
                        tstr = ''
        if tstr: ListMess.append(tstr)
    #---------------------------------------------------------------------------------------------------------------------------
        TupleMess = tuple(*ListMess,)
        if TMess not in ('ErrPoSh','Success'):
            if _LogFile:FileWrite(_LogFile,TupleMess)
            # if  LogFile:FileWrite( LogFile,tuple(ListMess))
        #------------------------------------------------------------------------------------------------
        if TMess == 'ErrPoSh':
            if  ErrFile:FileWrite( ErrFile,(f'{dtstr} ; {RMess}',))
            if _ErrFile:FileWrite(_ErrFile,(f'{dtstr} ; {RMess}',))
        #------------------------------------------------------------------------------------------------
        if TMess == 'Success':
            if  ResFile:FileWrite( ResFile,(f'{dtstr} ; {RMess}',))
            if _ResFile:FileWrite(_ResFile,(f'{dtstr} ; {RMess}',))
        #------------------------------------------------------------------------------------------------
        if debug: rpn(f'{dtstr} ; [yellow]{RMess}')
    except Exception as Err:
        Led = False
        if debug:rpn(str(Err))
    else:
        Led = True
    return Led
################################################################################################################################################################
def GetLstHPath(TemplUser:str, TermServer:str)->dict[str,list[str]] :
    """ Получение списка домашних папок юзверей на терминальном сервере"""
    LogErrDebug('Message',f'{TermServer = }', 'GetLstHPath')
    ListHP = {}
    #--------------------------------------------------------------------{TemplUser}%
    try:
        pc = WMI(TermServer)
        wql = f"SELECT LocalPath, Loaded FROM Win32_UserProfile WHERE '%{TemplUser}%' like LocalPath"
        qrt = pc.query(wql)
        if len(qrt):
            for ius in qrt:
                ListHP[os.path.basename(ius.LocalPath).lower()] = (ius.LocalPath,ius.Loaded)
        LogErrDebug('Message',f'По данному шаблону {TemplUser} обнаружено {len(qrt)} учетных записей','GetLstHPath')
    except Exception as Less:
        LogErrDebug('Failure',f'{Less}','UserHomePath')
        LogErrDebug('Failure',f'{traceback.format_exc()}','GetLstHPath')
    else:
        ResHP = dict(sorted(ListHP.items()))
        # LogErrDebug('Success',f'Список профилей :{ResHP} ','GetLstHPath')
    return ResHP
################################################################################################################################################################
if __name__ == '__main__':
    debug = True
    rpn(f"Модуль создания SymLink для IAS : {os.path.basename(__file__)} ver: {_VERSION} от {_VERDATE} автор {_AUTHOR}\n")
    #---------------------------------------------------------------------------------------------------------------------------
    # FileWrite( LogFile,('*'*_GlobaLen,))
    FileWrite(_LogFile,('*'*_GlobaLen,))
    if os.path.isfile( ErrFile):
        FileWrite( ErrFile,('*'*_GlobaLen,))
        FileWrite( ErrFile,('Нет ЛОКАЛЬНОЙ папки настройки 1С - Пользователь ни разу не запускал 1С из RDP сессии',))
    if os.path.isfile(_ErrFile):FileWrite(_ErrFile,('*'*_GlobaLen,))
    if os.path.isfile( ResFile):FileWrite( ResFile,('*'*_GlobaLen,))
    if os.path.isfile(_ResFile):FileWrite(_ResFile,('*'*_GlobaLen,))
    #--------------------------------------------------------------------------------------------------------------------------------------
    BlackList = ('omc170ge','omc170gp','omc20p17','omc20p26','omp21222')
    LogErrDebug('Message',f'Запуск модуля создания SymLink: {_VERSION} ; от {_VERDATE} ; автор {_AUTHOR}', os.path.basename(__file__))
    LogErrDebug('Message',f'{BlackList = }','Main')
    SrvDict = { 'AK-VDS-01.ak.local':r'\\AK-VDS-01.ak.local\ibases',
                'sh-vds-01.shumeiko.local':r'\\sh-vds-01.shumeiko.local\ibases',
                'SH-VDS-FRAN01.shumeiko.local':r'\\SH-VDS-FRAN01.shumeiko.local\ibases'}
    # SrvList = ("cl-33",)
    #--------------------------------------------------------------------------------------------------------------------------------------
    for ti,netibis in SrvDict.items():
        rpn(f'[cyan]{ti}')
        if input('\tОбработать профили на терминале [Y]/N:> ') not in ('Y','y','Д','д',''):continue
        LogErrDebug('Message',f'Обработка профилей на сервере {ti}','Main')
        # lpf = GetLstHPath(r'\o',ti)
        lpf = GetLstHPath('ias',ti)
        rpn(f'\t{'  UserID':7}   1cestart.cfg symlink  ib*.cfg')
        #-----------------------------------------------------------------------------------------------
        for usid,ilpl in lpf.items():
            # if debug:rpn(f'{usid = }',end='')
            if usid[:8].lower() in BlackList:
                LogErrDebug('ErrPoSh',f'{usid:17} клиент из списка исключений','Main')
                continue
            #-----------------------------------------------------------------------------------------
            NetUserCfg = fr'\\{ti}\{ilpl[0].replace(':','$')}\AppData\Roaming\1C\1CEStart'
            if not os.path.isdir(NetUserCfg):
                LogErrDebug('ErrPoSh',f'{ti} ; {usid:17} Нет папки настройки 1С','Main')
                continue
                # os.makedirs(NetUserCfg,exist_ok=True)
            NetUserCfg = os.path.join(NetUserCfg,'1cestart.cfg')
            if (sym := os.path.islink(NetUserCfg)):
                rpn(f'\t{usid:17}[green1]СимЛинк уже существует')
                LogErrDebug('Success',f'{ti} ; {usid:17} СимЛинк уже существует','Main')
                continue
            #-------------------------------------------------------------------------------------------
            # netibis = fr'{ibapath}\{usid[:8]}'
            if os.path.isdir(os.path.join(netibis,'OMC_ibases')):
                netibis = os.path.join(netibis,usid[:8])
            if not (rt := os.path.isdir(netibis)):
                LogErrDebug('ErrPoSh',f'{ti} ; {usid:17} Нет папки клиента на ibases','Main')
                continue
            cfgFile = fr'{netibis}\1cestart_{usid}.cfg'
            if not (rt := os.path.isfile(cfgFile)):
                LogErrDebug('ErrPoSh',f'{ti} ; {usid:17} Нет файла 1cestart_{usid}.cfg на ibases','Main')
                continue
            #----------------------------------------------------------------------------------------------
            try:
                if not debug:
                    if os.path.isfile(NetUserCfg) and not os.path.islink(NetUserCfg):
                        # pass
                        os.rename(NetUserCfg,f'{os.path.dirname(NetUserCfg)}\\1cestart_cfg.txt')
                    os.symlink(cfgFile, NetUserCfg)
                    LogErrDebug('Success',f'{ti} ; {usid:17} СимЛинк создан','Main')
                else:rpn(f'{debug = }')
                rpn(f'\t{usid:16} {os.path.isfile(NetUserCfg)} \t {sym} \t {rt} \t[cyan1]Симлинк создан')
            except Exception as Mess:
                rpn(f'[orchid]Ошибка: [yellow]{Mess}')
                rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
                LogErrDebug('Failure',f'{Mess}','UserHomePath')
                LogErrDebug('Failure',f'{traceback.format_exc()}','GetLstHPath')
            #-------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------
    input('Enter выход:-> ')
    LogErrDebug('Message',f'Выход {os.path.basename(__file__)}','Main')
    os._exit(0)
else:
    pass
