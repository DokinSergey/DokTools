import os
import traceback
from wmi import WMI
from rich import print as rpn
from datetime import datetime,timezone,date,timedelta
#--------------------------------
_AUTHOR  = 't.me/dokin_sergey'
_VERSION = '1.0.5'
_VERDATE = '2024-05-29 12:25'
#---------------------------------------------
ibapath = r'\\moscow\ibases'
# SRKpath = r'\\more\COPY\_log\psql-dump-enabled'
SrvList = ("cl-15", "cl-25", "cl-33","cl-35","cloud", "cloud-vip",'OMC22207', "bali","Baikal")
# SrvList = ("cl-33",)
LogFile = os.path.join(os.path.realpath(''),'log_')
ErrFile = os.path.join(os.path.realpath(''),'err_')
ResFile = os.path.join(os.path.realpath(''),'Res_')
# _LogFile = _ErrFile = _ResFile = ''
_USERNAME= os.getlogin()
_GlobaLen = 140
################################################################################################################################################################
try:
    # global _LogFile,_ErrFile,_ResFile
    _LogFile = f'{LogFile}{str(date.today())}.txt'
    _ErrFile = f'{ErrFile}{str(date.today())}.txt'
    _ResFile = f'{ResFile}{str(date.today())}.txt'
    with open(_LogFile, mode = 'a', encoding = 'utf_8') as sn:
        print('*' * _GlobaLen, file = sn)
    if os.path.isfile(_ErrFile):
        with open(_ErrFile, mode = 'a', encoding = 'utf_8') as sn:
            print('*' * _GlobaLen, file = sn)
    if os.path.isfile(_ResFile):
        with open(_ResFile, mode = 'a', encoding = 'utf_8') as sn:
            print('*' * _GlobaLen, file = sn)
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
        lFN = 17
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
        if _LogFile and TMess != 'ErrPoSh':
            with open(_LogFile, mode = 'a', encoding = 'utf_8') as fh:
                for ims in ListMess:
                    print(f'{PrnStr}{ims}', file = fh)
        #------------------------------------------------------------------------------------------------
        if _ErrFile and TMess == 'ErrPoSh':
            with open(_ErrFile, mode = 'a', encoding = 'utf_8') as fh:
                for ims in ListMess:
                    print(f'{dtstr} ; {RMess}', file = fh)
        #------------------------------------------------------------------------------------------------
        if _ResFile and TMess == 'Success':
            with open(_ResFile, mode = 'a', encoding = 'utf_8') as fh:
                for ims in ListMess:
                    print(f'{dtstr} ; {RMess}', file = fh)
        #------------------------------------------------------------------------------------------------
    except Exception as Err:
        Led = False
        if debug:rpn(str(Err))
    else:
        Led = True
    return Led
################################################################################################################################################################
def GetListHomePath(TemplUser:str, TermServer:str)->dict[str,list[str]] :
    """ Получение списка домашних папок юзверей на терминальном сервере"""
    LogErrDebug('Message',f'{TermServer = }', 'GetListHomePath')
    ListHP = {}
    #--------------------------------------------------------------------
    try:
        pc = WMI(TermServer)
        wql = f"SELECT LocalPath, Loaded FROM Win32_UserProfile WHERE '%{TemplUser}%' like LocalPath"
        qrt = pc.query(wql)
        if len(qrt):
            for ius in qrt:
                ListHP[os.path.basename(ius.LocalPath).lower()] = (ius.LocalPath,ius.Loaded)
        LogErrDebug('Message',f'По данному шаблону {TemplUser} обнаружено {len(qrt)} учетных записей','GetListHomePath')
    except Exception as Less:
        LogErrDebug('Failure',f'{Less}','UserHomePath')
        LogErrDebug('Failure',f'{traceback.format_exc()}','GetListHomePath')
    else:
        ResHP = dict(sorted(ListHP.items()))
        # LogErrDebug('Success',f'Список профилей :{ResHP} ','GetListHomePath')
    return ResHP
################################################################################################################################################################
###################################################################################################################
if __name__ == '__main__':
    debug = True
    rpn(f"Модуль создания SymLink : {os.path.basename(__file__)} ver: {_VERSION} от {_VERDATE} автор {_AUTHOR}\n")
    # logini()
    LogErrDebug('Message',f"Автономный Тест модуля логгирования: {_VERSION} ; от {_VERDATE} ; автор {_AUTHOR}",os.path.basename(__file__))
    BlackList = ('omc170ge','omc170gp','omc20p17','omc20p26','omp21222')
    for ti in SrvList:
        rpn(f'[cyan]{ti}')
        if input('\tОбработать профили на терминале [Y]/N:> ') not in ('Y','y','Д','д',''):continue
        lpf = GetListHomePath(r'\o',ti)
        # lpf = GetListHomePath(r'dev',ti)
        rpn(f'\t{'  UserID':7}   1cestart.cfg symlink  ib*.cfg')
        #-----------------------------------------------------------------------------------------------
        for usid,ilpl in lpf.items():
            if usid[:8].lower() in BlackList:
                LogErrDebug('ErrPoSh',f'{usid:17} клиент из списка исключений','Main')
                continue
            #-----------------------------------------------------------------------------------------
            NetUserCfg = fr'\\{ti}\{ilpl[0].replace(':','$')}\AppData\Roaming\1C\1CEStart\1cestart.cfg'
            if (sym := os.path.islink(NetUserCfg)):
                rpn(f'\t{usid:17}[green1]СимЛинк уже существует')
                LogErrDebug('Success',f'{ti} ; {usid:17} СимЛинк уже существует','Main')
                continue
            #-------------------------------------------------------------------------------------------
            netibis = fr'{ibapath}\{usid[:8]}'
            if not (rt := os.path.isdir(netibis)):
                LogErrDebug('ErrPoSh',f'{ti} ; {usid:17} Нет папки клиента на ibases','Main')
                continue
            cfgFile = fr'{netibis}\1cestart_{usid}.cfg'
            if not (rt := os.path.isfile(cfgFile)):
                LogErrDebug('ErrPoSh',f'{ti} ; {usid:17} Нет файла 1cestart_{usid}.cfg на ibases','Main')
                continue
            #----------------------------------------------------------------------------------------------
            try:
                if os.path.isfile(NetUserCfg) and not os.path.islink(NetUserCfg):
                    os.rename(NetUserCfg,f'{os.path.dirname(NetUserCfg)}\\1cestart_cfg.txt')
                os.symlink(cfgFile, NetUserCfg)
                rpn(f'\t{usid:16} {os.path.isfile(NetUserCfg)} \t {sym} \t {rt} \t[cyan1]Симлинк создан')
                LogErrDebug('Success',f'{ti} ; {usid:17} СимЛинк создан','Main')
            except Exception as Mess:
                rpn(f'[orchid]Ошибка: [yellow]{Mess}')
                rpn(f'[orchid]Ошибка: [yellow]{traceback.format_exc()}')
                LogErrDebug('Failure',f'{Mess}','UserHomePath')
                LogErrDebug('Failure',f'{traceback.format_exc()}','GetListHomePath')
            #-------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------
    input(':-> ')
    os._exit(0)
else:
    pass
