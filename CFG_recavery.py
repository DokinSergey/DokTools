import os
import chardet
import traceback
from glob import glob
from rich import print as rpn
###################################################################################################################
def RecoverAllCfg(cfgpath:str)->bool:
    cfgfile  = fr'{cfgpath}\_OMC_ibases_\1cestart.cfg'
    file_cfg = fr'{cfgpath}\OMC_ibases\1cestart.cfg'
    BaseDict:dict[str,str] = {}
    filelist:list[str] = []
    # rpn(f'[cyan2]Проверка файла [bright_green]{CfgName}[cyan2] на валидность')
    try:
        tmplv8i = r'*/ibases*.v8i'
        nf = 0
        for v8ifile in glob(tmplv8i,root_dir=cfgpath, recursive=True):
            if v8ifile[:3] == 'dev':continue
            nf +=1
            fullv8i = os.path.join(cfgpath,v8ifile)
            v8id = os.path.splitext(os.path.basename(v8ifile))[0].split('_',1)[-1]
            rpn(f'{nf:5} {v8ifile}')
            BaseDict.setdefault(v8id.lower(),fullv8i.lower())
        ## -------------------------------------------------------------------------------------------------------------
        rpn(BaseDict)
        rpn(len(BaseDict))
        with open(file_cfg, mode='rb') as fb:
            rk = chardet.detect(fb.read(256))['encoding']
        with open(file_cfg, mode = 'r', encoding = rk) as ecfg:
            for fstr in ecfg:
                if fstr[:16] == 'CommonInfoBases=':
                    if (bfid := os.path.splitext(os.path.basename(fstr[16:]))[0].split('_',1)[-1]):
                        if bfid.lower() not in BaseDict:
                            rpn(bfid)
                else:filelist.append(fstr)
        rpn(filelist)
            
            # if os.path.isfile(CfgName):
                # rk = DetectCodec(CfgName)
                # with open(CfgName, mode ='r', encoding = rk) as Hcfg: #, encoding='utf_16_le'
                    # filetxt = Hcfg.readlines()
            #------------------------------------------------------------------------------------
                # for istr in filetxt: # а теперь принимаемся за 1cestart.cfg
                    # if istr.startswith('CommonInfoBases='):
                        # ifile = istr.split('=')[1].strip()
                        # if os.path.isfile(ifile):
                            # vpath,vfile = os.path.split(ifile)
                            # BaseList.setdefault(vfile,vpath)
                        # else:
                            # rpn(f'[orange1]{ifile} [cyan2]Файл отсутсвует по указанному пути')
                            # print(f'{ifile}; Файл отсутсвует по указанному пути' ,file = ecfg )
#------------------------------------------------------------------------------
            # PathNotList = ('OMC_ibases','_OMC_temp','_OMC_temp','test')
            # for vpath, _, files in os.walk(CfgPath):
                # if len(vpath.split('\\')) > 4 and (vpath.split('\\')[4] in PathNotList):continue
                # # rpn(f'{root = }')
                # for vfile in files:
                    # if os.path.basename(vfile)[-3:] != 'v8i':continue
                    # # res = IIList.setdefault(vfile,vpath))
                    # if vfile in BaseList:#.keys():
                        # rpn(f'[green1]{os.path.realpath(os.path.join(vpath,vfile))}В словаре ')
                    # else:
                        # BaseList[vfile] = vpath
                        # rpn(f'[orange1]{os.path.realpath(os.path.join(vpath,vfile))}[cyan2] ссылка на файл отсутсвует ')
                        # print(f'{os.path.realpath(os.path.join(vpath,vfile))}; ссылка на файл отсутсвует' ,file = ecfg )
        # rpn(IIList)
        # получаем словар .v8i  с путями
        # V8iPath = f"{CfgPath}\\*\\*.v8i"
        # V8itempl = '*.v8i'
        # filetxt = glob(V8itempl, root_dir=CfgPath, recursive=True)
        # rpn(f'{filetxt = }')
        # for istr in filetxt:
            # vPath,vfile = os.path.split(istr.strip())
            # BaseList.setdefault(vfile,vPath)
        # rpn(BaseList)
    #---------------------------------------------------------------
        ab = True
    except Exception as DErr:
        rpn('ErrMess',f'{str(DErr)} ; {cfgpath = }')
        ab = False
    return ab
########################################################################################################################


########################################################################################################################
if __name__ == '__main__':
    RecoverAllCfg(r'\\moscow\ibases')#\OMC_ibases\1cestart.cfg
    input('Выход :-)>')
