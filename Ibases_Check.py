import os
import chardet
import traceback
from datetime import datetime,timedelta
from rich import print as rpn

#---------------------------------------------------
__author__  = 't.me/dokin_sergey'
__version__ = '0.0.0'
__verdate__ = '2025-04-07 13:10'
kGb = 1048576
#########################################################################################################################################
def get_code(FileName:str)->str:
    try:
        if not os.path.isfile(FileName):
            rpn(f'\t Файл {FileName} недоступен')
            return ''
        with open(FileName, mode='rb') as fb:
            rawdata = fb.read(512)
        if len(rawdata) < 5:return ''
        rk = chardet.detect(rawdata)['encoding']
    except Exception as Mess:
        rpn(f'\t get_code[orchid]: {Mess}')
        rpn(f'\t get_code[orchid]: {traceback.format_exc()}')
    return rk
#########################################################################################################################################
def file_list(defpatg:str)->dict[str,dict[str,str]]:
    filelist = {}
    try:
        if not os.path.isdir(defpatg):
            return filelist
        #---------------------------------------
        with os.scandir(defpatg) as pa:
            for iit in pa:
                if iit.is_file():
                    rk = get_code(iit)
                    # fn = os.path.basename(iit).{ft}
                    fstat = iit.stat()
                    ft = datetime.fromtimestamp(fstat.st_ctime)
                    fm = datetime.fromtimestamp(fstat.st_mtime)#дата редактирования
                    tmd = timedelta(0,1)
                    fd = fm-ft
                    fms = fm.strftime("%Y-%m-%d %H:%M:%S") if fd > tmd else '\t\t'
                    rpn(f'\t[cyan1] {iit.name:40}[green1]{rk:9}[cyan1] {fstat.st_size:6}\t \t{fms}')# \t{fd<tmd} \t{fd}')
#---------------------------------------------
    except Exception as Mess:
        rpn(f'\tfile_list[orchid]: {Mess}')
        rpn(f'\tfile_list[orchid]: {traceback.format_exc()}')
    return filelist
#########################################################################################################################################
if __name__ == '__main__':
    debug = True
    a = ''
    tpath = r'\\sh-vds-01\ibases'
    try:
        while not a:
            rpn(f'Старт процесса для [green1]{tpath}\n')
            file_list(tpath)
            a = input('Повтор :-> ')
#---------------------------------------------
    except Exception as Mess:
        rpn(f'\t[bright_red]Ошибка: {Mess}')
        rpn(f'\t[bright_red]Ошибка: {traceback.format_exc()}')
    os._exit(0)
