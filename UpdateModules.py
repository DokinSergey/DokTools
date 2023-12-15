import os
from rich import print
from subprocess import Popen, PIPE#,SubprocessError,TimeoutExpired
__version__ = '1.0.0'
__verdate__ = '2023-12-15 10:39'
print('Обновление модулей Python') 

try:
    os.chdir(r'C:\Program Files\Python312\Scripts')
    with Popen(['pip', 'list','-o'], shell=True, stdout = PIPE, stderr = PIPE) as popps:
        pls = popps.communicate(timeout=15)
    if bool(pls[1]):
        print('Error:')
        print(pls[1].decode('cp866'))
    if  bool(pls[0]):
        restxt = (pls[0].decode('cp866')).splitlines()[2:]
        print('Доступны для обновления')
        print(restxt)
        if input('Обновить?:> '): raise Exception ('Нет, так нет')
        for it in restxt:
            print()
            tprg = it.split()[0]
            print(f'Модуль {tprg} версии {it.split()[1]}')
            with Popen(['pip','install','-U',f'{tprg}'], shell=True, stdout = PIPE, stderr = PIPE) as popps:
                pls = popps.communicate(timeout=15)
            if bool(pls[1]):
                print('Error:')
                print(pls[1].decode('cp866'))
            if  bool(pls[0]):
                print(pls[0].decode('cp866'))
    else:
        print('Все модули последней версии')
except Exception as Ers:
    print(str(Ers))
