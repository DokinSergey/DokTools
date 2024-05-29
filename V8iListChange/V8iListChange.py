# from dataclasses import dataclass, field
from rich import print 
import os, glob, csv, logging, traceback 
#----------------------------------------
version = '1.0.2.7'
verdate = '2023-06-21 16:43:53'

class V8iExcept(BaseException):
    def __init__(self, message):
        super().__init__(message)

# ListBaseChange =("dev22001-acc-fxnxufcy",)
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
#######################################################################################
if __name__ == '__main__':
    ScriptPath = os.path.realpath('')
    FileLogMod = ScriptPath +"/loggin.txt"
    FileCsv = ScriptPath + '\listv8i.csv'    
    with open(FileLogMod, mode = 'a') as fh:
        print('-' * 130, file = fh)
    #------------------------------------------------------------------------------------------------------------------------------------------
    logging.basicConfig(level=logging.INFO, filename = FileLogMod, encoding='utf-8', filemode = "a", style='{', #по умолчанию = "a" append
                format = "{asctime};{process:x} ;{message}", datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Запуск: стартовый файл {FileCsv}')             
    #------------------------------------------------------------------------------------------------------------------------------------------ 
    FileCsv = ScriptPath + '\listv8i.csv'
    try:
        #-----------------------------------------------------------------------
        while not os.path.exists(FileCsv):
            print('Что-то файла не видно. Введём вручную?')
            print('Если указать имя без пути поиск будет') 
            print(f'в папке со скриптом {ScriptPath}')         
            inkey = input("Имя файла(0 - выход): ")
            logging.info(f'ВВод пользователя с клавиатуры {inkey}')  
            if inkey == '0':
                raise V8iExcept('Пользователь нажал "0". Выход') 
            elif os.path.isabs(inkey): #Это длинный путь?
                FileCsv = inkey
            else:
                FileCsv = ScriptPath +'\\'+ inkey
        print(f"[bright_yellow]{FileCsv}")    
        logging.info(f"фактический файл {FileCsv}")
        #-------------------------------------------------------------------------
        FlDict = {}
        with open(FileCsv, mode = 'r', newline='') as hcsv:
            CsvLine = list(csv.reader(hcsv, delimiter=';'))
        # print(CsvLine)
        CountLineCSV = len(CsvLine)
        CountFileFact = 0
        for LineTxt in CsvLine:
            logging.info(f"CSV: {LineTxt}")
            iList = []
            for itr in range(len(list(LineTxt))):
                if itr == 0: 
                    iKey = list(LineTxt)[itr].strip().lower()
                    if iKey in  FlDict.keys():
                        print(f'[bright_red] База {iKey} уже добавлена в список')
                        continue
                if itr  > 0: iList.append(LineTxt[itr].strip());
                FlDict.setdefault(iKey,iList)                
        # print(FlDict)
        #-------------------------------------------------------------------------------------------------------
        IbasesPath = '\\\\moscow\\ibases' #\\*\\*.v8i'
        # IbasesPath = 'S:\ibases_test'
        # print(IbasesPath)
        print('Файд CSV прочитан.')
        kstr = None
        while kstr not in ('Y', 'y'):
            print(f"Базовый путь: [cyan3]{IbasesPath}")
            kstr = input('Продолжить(Y), Изменить баз.папку(I) Выйти[N]: ')
            if kstr in ('N', 'n', ''):
                raise V8iExcept('Решение пользователя - Выход')
            elif kstr in ('I', 'i'):
                print('[cyan1]К новому пути будет добавлен шаблон [bright_yellow]"\\*\\*.v8i"')
                iNF = input('Введите базовый путь: ')
                if os.path.isdir(iNF): 
                    IbasesPath = iNF.strip().rstrip('\\')
                else: 
                    print(f'{iNF} не является правильным путём')
        IbasesPath += '\\*\\*.v8i'
        print(f'{IbasesPath}')
        logging.info(f"Шаблон поиска файлов {IbasesPath}")
        # input("Нажмите ENTER для продолжения: ")
        #-----------------------------------------------------------------------------------------------------
        BaseList = glob.glob(IbasesPath, recursive = True)        
        # print(BaseList)
        for iIB in BaseList:
            indNB = iIB.rsplit('_', maxsplit=1)[1]
            NameBase = indNB[:-4].lower()
            # print (NameBase)
            #---------------------------------------------------------- Разбор файла на косточки
            ConnFile = False
            if NameBase in FlDict.keys():
                logging.info(f"{iIB} - Файл в списке ")
                print(f"[cyan1]{iIB}", end='')
                rk = DetectCodec(iIB)
                #if not rk: rk = "utf_8"
                with open(iIB, mode ='r', encoding = rk) as Hg:
                    v8itxt = Hg.read()
                # print(v8itxt.splitlines())
                countv8i = 0; fVersion = ''; fAddParam = ''; fAppArch = ''
                for lntxt in v8itxt.splitlines():
                    if lntxt.startswith('Connect='): countv8i += 1
                    if lntxt.startswith('['): fBasName = lntxt.strip('[]').strip()
                    elif lntxt.startswith('Connect=File'): ConnFile = True
                    elif lntxt.startswith('Connect=Srvr'):
                        fServer = lntxt.split(';')[0].split('=')[2].strip('"')
                        fBaseID = lntxt.split(';')[1].split('=')[1].strip('"')
                    elif lntxt.startswith('ID='): fID = lntxt.strip('ID=')
                    elif lntxt.startswith('Folder='): fFolder = lntxt.strip('Folder=/')
                    elif lntxt.startswith('Version='): fVersion = lntxt.strip('Version=')
                    elif lntxt.startswith('AdditionalParameters='): fAddParam = lntxt.strip('AdditionalParameters=')
                    elif lntxt.startswith('AppArch='): fAppArch = lntxt.strip('AppArch=')
                if ConnFile: 
                    logging.info(f'{iIB} - файловые базы не обрабатываются')
                    print('[orange1] - файловые базы не обрабатываются')
                    continue
                if (countv8i - 1):
                    logging.info(f'{iIB} - файл содержит ссылку на более чем 1 базу, обработка не возможна')
                    print(f'[orange1] - файл содержит ссылку на более чем 1 базу, обработка не возможна')
                    continue
                print ('[green3] - успешно')    
                logging.info(f'Old:{fBasName=} {fServer=}{fBaseID=}{fVersion=}{fAddParam=}{fAppArch=}')
                #---------------------------------------------------------------- замена значений
                v8itml = f'[{fBasName} ]\n'
                if len(FlDict[NameBase]) > 0 and FlDict[NameBase][0]: 
                    v8itml += f'Connect=Srvr="{FlDict[NameBase][0]}";Ref="{fBaseID}";\n'
                else:
                    v8itml += f'Connect=Srvr="{fServer}";Ref="{fBaseID}";\n'
                v8itml += f'ID={fID}\n'
                v8itml += f'Folder=/{fFolder}\n'
                v8itml += f'External=1\n'
                v8itml += f'ClientConnectionSpeed=Normal\n'
                v8itml += f'App=Auto\n'
                v8itml += f'WA=1'

                if len(FlDict[NameBase]) > 1 and FlDict[NameBase][1]:
                    v8itml += f'\nVersion={FlDict[NameBase][1]}'
                elif fVersion:
                    v8itml += f'\nVersion={fVersion}'
                    
                if len(FlDict[NameBase]) > 2 and FlDict[NameBase][2]: 
                    v8itml += f'\nAppArch={FlDict[NameBase][2]}'
                elif fAppArch:
                    v8itml += f'\nAppArch={fAppArch}'
                    
                if len(FlDict[NameBase]) > 3 and FlDict[NameBase][3]:
                    v8itml += f'\nAdditionalParameters={FlDict[NameBase][3]}'
                elif fAddParam:
                    v8itml += f'\nAdditionalParameters={fAddParam}'
                    
                logging.info(f'New:{fBasName=}{fServer=}{fBaseID=}{fVersion=}{fAddParam=}{fAppArch=}')
                #---------------------------------------------------------------- сохраняем
                nIB = f'{iIB[0:-3]}old'
                inf = 1
                while os.path.exists(nIB):
                    nIB = f'{iIB[0:-4]}_{str(inf)}.old'
                    inf += 1
                os.rename(iIB, nIB)
                # print(nIB)
                # print(v8itml) 
                # iIB = iIB.lower()
                with open(iIB, mode ='w', encoding='utf_8') as V8n:
                    print(v8itml, file = V8n)
                    # V8n.write(v8itml.format(tBasName = fBasName, tServ1c = fServer, tBas = fBaseID, tGuID = fID,
                        # tBaseUsrFldr = fFolder, tVers = fVersion, tAddParam = fAddParam, tArch = fAppArch))
                CountFileFact += 1
        #-----------------------------------------------------------------------------------------------------------------------------------------------
    except V8iExcept as Mess:
        logging.info(str(Mess))
    except Exception as Derr:
        print(f"[bright_red]{Derr}")
        logging.warning(str(Derr))
        print(f"[bright_red]{traceback.format_exc()}")
        logging.warning(str(traceback.format_exc()))
        #-------------
        AA_Mess = Derr
    else:
        # print(f"[cyan3]В файле {FileCsv} задано {CountLineCSV} файлов")
        print(f"[green3]Успешно обработано {CountFileFact} [orange1]из {CountLineCSV} файлов")
        logging.info(f'Обработано без ошибок {CountFileFact} из {CountLineCSV} файлов')
    finally:
        logging.info('Выход из программы ')
        input("Нажмите ENTER для закрытия окна: ")