# pylint: disable-msg=W0611
import os
import csv
import traceback
import sys
from glob import glob
from rich import print
from datetime import date,datetime,timezone,timedelta
from subprocess import Popen, PIPE,SubprocessError,TimeoutExpired
#--------------------------------
_AUTHOR  = 't.me/dokin_sergey'
_VERSION = '1.1.1'
_VERDATE = '2024-04-22 20:10'
#----------------------------------------------------------------------------
class OmcExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#----------------------------------------------------------------------------
LogFile = fr'{os.path.dirname(__file__)}\{str(date.today())}.txt'
with open(LogFile, mode ='a', encoding = 'utf_8') as hlog:
    print('*'*50, file = hlog)
#######################################################################################
def DetectCodec(FlNm:str)->str:
    """Определение параметров кодировки файла.
    главное определить utf_16 и utf_8 с BOB. Остальное определяется само"""
    DetCode = ''
    with open(FlNm, mode ='rb') as bfl:
        br = bfl.read(3)
        if   bool(br) and (br[0] + br[1] == 509): DetCode = "\'utf_16\'"
        elif bool(br) and (br[0] + br[1] == 426): DetCode = "\'utf_8_sig\'"
        else: DetCode = 'utf_8'
    return DetCode
#########################################################################################################################################
def PSExec(ps_str:str)->str:
    res = ''
    try:
        with Popen(['powershell', ps_str], stdout = PIPE, stderr = PIPE, encoding="cp866") as popps:
            pls = popps.communicate(timeout=15)
        if bool(pls[1]):
            print(f'[yellow]PowerShell {pls[1]}')
        res = str(pls[0])
        # print(res)
    except TimeoutExpired as Mess:
        print(f'[orchid]TimeoutExpired {Mess}')
    except SubprocessError as Mess:
        print(f'[orchid]SubprocessError {Mess}')
    except Exception as Mess:
        print(f'[orchid]SubprocessError {Mess}')
        print(f'[orchid]SubprocessError {traceback.format_exc()}')
    # else:
    return res
#########################################################################################################################################
def Loging(Mess:str):
    try:
        dtnow = datetime.now(timezone.utc) + timedelta(hours=3)
        dtstr = dtnow.strftime("%H:%M:%S")
        with open(LogFile, mode ='a', encoding = 'utf_8') as tlog:
            print(f'{dtstr}:{Mess}', file = tlog)
    except Exception as LErr:
        print(f'\t[orchid]{LErr}')
        print(f'\t[bright_yellow]{traceback.format_exc()}')
#########################################################################################################################################
def OptFileCsv(Ppath:str)->str:
    res = ''
    filetxt = glob('*.csv', root_dir=Ppath, recursive=True)
    # for tfls in iglob('*.csv', root_dir=Ppath, recursive=True):
    print(Ppath)
    for nn,tfls in enumerate(filetxt):
        print(f'[green1]{nn:2d}  [cyan1]{tfls}')
    while not ((nf:= input('Выберите Номер файла:-> ')).isdigit() and int(nf) in range(len(filetxt))):pass
    # print(f'\n\t[green1]{filetxt[int(nf)]}')
    res = filetxt[int(nf)]
    return res
#########################################################################################################################################
def SetUserComp(omcid:str, CmName:str)->str:
    res = False
    try:
        ps_str = f'''Get-ADUser -Server "1more" -Filter "Name -like '{omcid}*'" -Properties company | ft Name, company -HideTableHeaders \n'''
        psr = PSExec(ps_str).strip().splitlines()
        for lst in psr:
            sl = lst.split(' ',1)
            # print(sl)#[0],sl[1] )
            if (len(sl) == 1) or (len(sl) > 1 and sl[1] != CmName):
                ps_str = f'''Set-ADUser -Server "1more" -Identity "{sl[0]}" -Company "{CmName}" -Passthru | ft Name -HideTableHeaders \n'''
                ps_r = PSExec(ps_str).strip()#.splitlines()
                # print(ps_r)
                if ps_r:
                    print(f'\t\t [green1]{ps_r} {CmName}')
                    Loging(f'{ps_r};{sl[1]};{CmName}')
#-----------------------------------------------------------------------------------------------------------------------------------------
    except OmcExcept as MErr:
        print(f'[bright_yellow]{MErr}')
    except Exception as EErr:
        print(f'[orchid]{EErr}')
        print(f'[bright_yellow]{traceback.format_exc()}')
    else:
        res = True
    return res
#########################################################################################################################################
if __name__ == '__main__':
    print( '[green1]Скрипт установки полей Description и company в АД по списку')
    print(f'[green1]Версия [cyan1]{_VERSION} от {_VERDATE}')
    fcsv ='OMCAdComp.csv'
    fcsv ='OMC_Group.csv'
    CSVFile = fr'{os.path.dirname(__file__)}\{fcsv}'
    if not os.path.isfile(CSVFile):
        fcsv = OptFileCsv(os.path.dirname(__file__))
        if fcsv:CSVFile = fr'{os.path.dirname(__file__)}\{fcsv}'
        else:raise OmcExcept ('Выход оператором')
    print(f'[cyan1]Файл задания [green1]{CSVFile}')
    omcdct = {}
    try:
        if input('Выполнить:-> [Y] ? ') not in ('Y','y','Д','д',''):raise OmcExcept ('Выход оператором')
        if os.path.isfile(CSVFile):
            rk = DetectCodec(CSVFile)#, encoding='utf_8'
            with open(CSVFile, mode ='r', encoding = rk, newline='') as hcsv:
                CsvLine = list(csv.reader(hcsv, delimiter=';'))
        #----------------------------------------------------------------------------
            for ii,tcsv in enumerate(CsvLine):
                if ii and tcsv[1]:omcdct[tcsv[0]] = tcsv[1]
        #----------------------------------------------------------------------------
            for omid,oname in omcdct.items():
                print(f'\t[cyan1]{omid}',end='')
                if omid[:3].lower() == 'ias':
                    SetUserComp(omid,oname)
                    print()
                    continue
            #--------------------------------------------------------------------------------------------------------------
                # break
                psstr  =  'Import-Module ActiveDirectory \n'
                psstr += f'''$ado =Get-ADGroup -Server '1more' -Filter "Name -like '{omid}'" -Properties Description \n'''
                psstr += '$ADO.Name,$ADO.Description \n'
                # if len(rps := PSExec(psstr).split('\n')) == 2:# splitlines()) == 2:
                rps = PSExec(psstr)
                # print(f'{rps= }')
                if rps:
                    rs = rps.split('\n')
                    if len(rs) < 4:
                        if rs[1] != oname:
                            psstr = f'Set-ADGroup -Server "1more" -Identity "{omid}" -Description "{oname}" -Passthru | ft Name -HideTableHeaders \n'
                            rps = PSExec(psstr).strip()#.splitlines()
                            if rps:
                                print(f'[bright_blue] записано  [green1]{oname}')
                                Loging(f'{rs[0]}  ;{rs[1]};{oname}')
                        else:print()
                        SetUserComp(omid,oname)
                    else:
                        print('[yellow] обнаружено более одной записи')#Для {omid}
                else:
                    print('[yellow] записей не найдено')#Для {omid}
        #----------------------------------------------------------------------------
        else:
            print('Файла нетути')
            # sys.exit()
#----------------------------------------------------------------------------
    except OmcExcept as DErr:
        print(f'[bright_yellow]{DErr}')
    except Exception as DErr:
        print(f'[orchid]{DErr}')
        print(f'[bright_yellow]{traceback.format_exc()}')
    print()
    input('Закрыть окно:-> ')
    os._exit(0)
