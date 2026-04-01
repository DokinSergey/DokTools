#!/usr/bin/env python3
import shutil
import requests
import datetime

# Это переменные для запроса звонков и их записей. см. Описание тут https://wiki.sipnet.ru/index.php?title=API_для_интеграции_с_CRM
payload = {'operation': 'calls',      # Метод который возвращает статистику звонков и ссылки на записи.
          'D1': '00/00/2000',        # Если не правильная дата, то сегодня
          'D2': '00/00/2000',        # Если не правильная дата, то сегодня
          'sipuid': '<Login>',       # Тут логин или SIP-ID укажите
          'password': '<Password>',  # Тут конечно пароль нужен
          'format': '2'              # Это формат возвращаемых данных. Нам очень Json понравился
          }

# Это URL запроса статистики
url = 'https://api.sipnet.ru/cgi-bin/Exchange.dll/sip_balance'
# Теперь определим лимит числа скачиваемых файлов. Если это Maxgetfiles=0, то файлы не скачиваются
Maxgetfiles = 10

response= requests.post(url, data=payload)

if response.status_code == requests.codes.ok:
    dictionary=response.json()
    del response
    if dictionary["Result"]:
        # нам уже доступна структура данных ответа. Если хотите, напечатайте ее.
        # print ("Структура ответа ", dictionary.keys())
        if 'calls' in dictionary.keys():
            # нам уже доступна структура данных самого звонка. Если хотите, напечатайте ее.
            # print ("Структура звонков ", dictionary["calls"][1].keys())
            # print ("Структура [1] ", dictionary["calls"][1])
            # Далее цикл для обхода всех полученых звонков и печати отчета по ним.
            # Для вывода звонков от начала дня к текущему моменту
            # for i in dictionary["calls"]:
            for i in reversed(dictionary["calls"]):
                if 'phone' in i.keys():
                    print ("======================================================================================================")
                    print (i["cid"], '',"Дата= " ,i["gmt"],"Номер= ",i["phone"], "АОН= ", i["cli"], "Длительность= ", i["duration"])
                    print (str(datetime.datetime.utcnow()))
                else:
                    print ("Странный звонок у него нет номера B")
                if 'url' in i.keys():
                    # Это URL файла с записью разговора.
                    print (i["url"])
                    # Проверяем, не исчерпан ли лимит скачивания файлов
                    if Maxgetfiles>0:
                        # Скачаем и сохраним все обнаруженные записи имя сохраненного файла состоит из cid звонка.
                        response = requests.get(i["url"], stream=True)
                        if response.status_code == requests.codes.ok:
                            FileName = str(i["gmt"])+"_"+str(i["phone"])
                            if response.headers['Content-Type'] == 'audio/mpeg':
                                FileName = FileName+".mp3"
                            else:
                                FileName = FileName+".zip"
                            FileName = FileName.replace('/', '-').replace(':', '-')
                            with open(FileName, 'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            del response
                            Maxgetfiles -= 1
                        else:
                            print ("Запись не скачалась. Получили код ", response.status_code)
                    else:
                        print ("Лимит скачивания исчерпан")
                        break
                else:
                    print ("Нет MP3 записи этого звонка")
        else:
            print ("Результат нормальный, но Нет звонков")
    else:
        print ("Что-то пошло не так. Плохой результат получили ", dictionary["Result"])
else:
    print ("Совсем плохо. Получили код ", response.status_code)
