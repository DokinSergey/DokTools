import os
import traceback
# from rich import print
from shutil import rmtree
# from subprocess import Popen, PIPE,SubprocessError,TimeoutExpired
##################################################################################
class OmcExcept(Exception):
    def __init__(self, message):
        super().__init__(message)

class PowerShell(Exception):
    def __init__(self, message):
        super().__init__(message)
###################################################################################################################################
def DetectCodec(FlNm:str)->str:
    """Определение параметров кодировки файла.
    главное определить utf_16 и utf_8 с BOB. Остальное определяется само"""
    DetCode = ''
    with open(FlNm, mode ='rb') as bfl:
        br = bfl.read(3)
        if   bool(br) and (br[0] + br[1] == 509):
            DetCode = r"'utf_16'"
        elif bool(br) and (br[0] + br[1] == 426):
            DetCode = r"'utf_8_sig'"
        else: DetCode = None
    return DetCode
####################################################################################################################################
def v8iFileList(path1c:str)->list:
    exclist = []
    try:
        rk = DetectCodec(path1c)
        with open(path1c, mode ='r', encoding = rk) as Hcfg:
            filetxt = Hcfg.readlines() #Читаем файл одним куском
        #------------------------------------------------------------------------------------
        itertxt = iter(filetxt)  #преобразуем многострочный текс в итератор
        for istr in itertxt: # пошли по строкам
            if istr.startswith('Connect=File'): # нужнам нам строка в наличии
                a = next(itertxt).split('=')[1].strip()
                exclist.append(a) # ID из строки +1
                # LogErrDebug(f'{path1c = } ; ID={a}','v8iRead')
                # exclist.append(next(itertxt).split('=')[1].strip()) # ID из строки +1
            #---------- отладка ---------------------------------------------------------
                # print(a)# отладка убрать
            #----------------------------------------------------------------------------
    except Exception as DErr:
        print(f'v8iFileList Ошибка:> {str(DErr)}')
        print(traceback.format_exc())
    return exclist
###################################################################################################################################
pathlist = []
try:
    userpath = os.getenv('USERPROFILE')
    uspt = userpath
    print(f'[bright_green]{uspt}')
    f1c8i = fr'{uspt}\AppData\Roaming\1C\1CEStart\ibases.v8i'
    excpath = v8iFileList(f1c8i) if os.path.isfile(f1c8i) else []
    excpath.append('logs')
    excpath.append('ExtCompT')
    # excfile = ('1cv8.pfl','1cv8c.pfl','1cv8u.pfl','1cv8cmn.pfl','1cv8strt.pfl','appsrvrs.lst' )
    incpath1C = (r'AppData\Local\1C\1cv8',r'AppData\Local\1C\1Cv8ConfigUpdate',r'AppData\Roaming\1C\1cv8',r'AppData\Roaming\1C\1cv8')
    incpathtm = (r'AppData\Local\Temp',)
    #-------------------------------------------------------
    for apath in incpath1C:
        ipath = f'{uspt}\\{apath.strip("\\")}'
        print('\t',ipath)
        if os.path.isdir(ipath):
            for bpath in os.listdir(ipath):
                if os.path.isdir(f'{ipath}\\{bpath}') and bpath not in excpath:
                    cpath = f'{ipath}\\{bpath}'
                    # pathlist.append(cpath)
                    print('\t\tPt:', cpath)
                    rmtree(cpath, ignore_errors=True)
#-------------------------------------------------------------------
    ipath = fr'{uspt}\AppData\Local\Temp'
    print('\t',ipath)
    if os.path.isdir(ipath):
        rmtree(ipath, ignore_errors=True)
except OmcExcept as Mess:
    print(f'OmcExcept:> {str(Mess)}')
except Exception as Mess:
    print(f'Ошибка:> {str(Mess)}')
    print(traceback.format_exc())
else:
    print('Успешно')
