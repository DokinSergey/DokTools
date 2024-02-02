import os
# import time
import traceback
import glob
import datetime
# import json
# from subprocess import Popen, PIPE,SubprocessError,TimeoutExpired
# from dataclasses import dataclass #, field
# from shutil import copytree,ignore_patterns,disk_usage,copy2
# from wmi import WMI
from rich import print
#---------------------------------------------------
_AUTHOR  = 't.me/dokin_sergey'
_VERSION = '1.0.0'
_VERDATE = '2024-01-25 20:37'
_USERNAME = os.getlogin()
_COMPNAME = str(os.environ['COMPUTERNAME'])
_LogFile = f'{os.path.splitext(__file__)[0]}.log.txt'
_ResFile = f'{os.path.splitext(__file__)[0]}.txt'
#########################################################################################################################################
def LogErrDebug(RawMess:str, Funct:str = '')->str:
    # global _LogFile
    MesStr = f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")};{_COMPNAME};{_USERNAME};'
    lFN = 17
    FN = f'{Funct:{lFN}} ;' if Funct else f'{" ":{lFN}} ;'
    MesStr += FN
    MesStr += RawMess
    try:
        with open(_LogFile, mode = 'a', encoding = 'utf_8') as fh:
            print(MesStr, file = fh)
    except Exception as LErr:
        print(str(LErr))
    return ''
#########################################################################################################################################
def DetectCodec(FlNm:str)->str:
    """Определение параметров кодировки файла.
    главное определить utf_16 и utf_8 с BOB. Остальное определяется само"""
    DetCode = ''
    with open(FlNm, mode ='rb') as bfl:
        br = bfl.read(3)
        if   bool(br) and (br[0] + br[1] == 509):#FE + FF
            DetCode = r"'utf_16'"
        elif bool(br) and (br[0] + br[1] == 426):# EF + BB
            DetCode = r"'utf_8_sig'"
        else: 
            DetCode = None
            DetCode = r"'utf_8'"
    return DetCode
##########################################################################################################################################
def GetListFolder1C(IbasesPath:str)->list:
    res = []
    V8iPath = fr"{IbasesPath}\*\*.v8i"
    LogErrDebug(f'{IbasesPath}','GetListFolder1C')
    BaseList = glob.glob(V8iPath)
    #------------------------------------------------------------------------------------
    for val in BaseList:
        try:
            rk = DetectCodec(val)
            # print(f"{val} {rk = }")
            with open(val, mode ='r', encoding = rk) as Hcfg:
                filetxt = Hcfg.readlines()
            #------------------------------------------------------------------------------------
            # itertxt = iter(filetxt)  #преобразуем многострочный текс в итератор
            for istr in filetxt:#itertxt: # пошли по строкам
                if istr.startswith('Folder=/'): # нужнам нам строка в наличии
                    a = istr.split('/')[1].strip()
                    if a not in res:
                        res.append(a)
                    # print(f'\t{a = }')
        except Exception as DErr:
            print(str(DErr))
            LogErrDebug(f'{os.path.basename(val)} ; {rk =}','GetListFolder1C')
            LogErrDebug(f'{DErr}','GetListFolder1C')
            # LogErrDebug(f'{traceback.format_exc()}','GetListFolder1C')
    return res
###################################################################################################################################
if __name__ == '__main__':
    print(_LogFile)
    _mess = f"Запуск проверки файлов ibases ver:{_VERSION}; от:{_VERDATE} ; автор:{_AUTHOR}"
    print(_mess)
    LogErrDebug(f'{_mess};',os.path.basename(__file__))
    # rty = UserHomePath('OMC170%', 'bali')#.Mess1
    # print(rty)
    ytr = GetListFolder1C(r'\\moscow\ibases')
    ytr.sort(key=str.lower)
    with open(_ResFile, mode = 'w', encoding = 'utf_8') as rfh:
        for iIB, val in enumerate(ytr):
            if val:
                print(f'{iIB:3}: {val}')
                print(f'{iIB:3}: {val}', file = rfh)
    
else:
    LogErrDebug(f'{os.path.basename(__file__)} ; версии {_VERSION} ; от {_VERDATE}',os.path.basename(__file__))
