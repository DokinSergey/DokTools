#!/usr/bin/env python3
import shutil
import requests
import datetime
from multiprocessing import Pool

# Это переменные для запроса звонков и их записей. см. Описание тут https://wiki.sipnet.ru/index.php?title=API_для_интеграции_с_CRM
payload = {'operation': 'calls',      # Метод который возвращает статистику звонков и ссылки на записи.
          'D1': '00',        # Если не правильная дата, то сегодня
          'D2': '00',        # Если не правильная дата, то сегодня
          'sipuid': '<SIPID>',       # Тут логин или SIP-ID укажите
          'password': '<Password>',  # Тут конечно пароль нужен
          'format': '2'              # Это формат возвращаемых данных. Нам очень Json понравился
          }

# Это URL запроса статистики
url = 'https://api.sipnet.ru/cgi-bin/Exchange.dll/sip_balance'

# Теперь определим лимит числа скачиваемых файлов. Если это Maxgetfiles=0, то файлы не скачиваются
# Не работает в многопотоковом варианте.
#Maxgetfiles = 10

# Описываем процедуру скачивания записи разговора
def create_MP3file(callinfo):
   if 'phone' in callinfo.keys():
       print ("======================================================================================================")
       print (callinfo["cid"], '',"Дата= " ,callinfo["gmt"],"Номер= ",callinfo["phone"], "АОН= ", callinfo["cli"], "Длительность= ", callinfo["duration"])
       print ("Время в момент скачивания файла: ", str(datetime.datetime.utcnow()))
       if 'url' in callinfo.keys():
          # Это URL файла с записью разговора.
          print (callinfo["url"])
          # Скачаем и сохраним все обнаруженные записи имя сохраненного файла состоит из cid звонка.
          response = requests.get(callinfo["url"], stream=True)
          if response.status_code == requests.codes.ok:
              FileName = str(callinfo["gmt"])+"_"+str(callinfo["phone"])
              if response.headers['Content-Type'] == 'audio/mpeg':
                  FileName = FileName+".mp3"
              else:
                  FileName = FileName+".zip"
              FileName = FileName.replace('/', '-').replace(':', '-')
              with open(FileName, 'wb') as out_file:
                  shutil.copyfileobj(response.raw, out_file)
              del response
          else:
              print ("Запись не скачалась. Получили код ", response.status_code)
       else:
           print ("Нет MP3 записи этого звонка")
   else:
       print ("Странный звонок у него нет номера B")

# Это основной метод, который получает список звонков и запускает многопотоковое скачивание
if __name__ == '__main__':
   print ("Начало исполнения: ", str(datetime.datetime.utcnow()))
   # Это создание пула исполнителей, которые будут скачивать записи
   # Число исполнителей нужно выбирать под компьютер, на котором выполняется. У меня 1500 записей скачались менее чем за 2 минуты
   pool = Pool(10)
   # Запрос статистики со ссылками на файлы записи разговоров
   response = requests.post(url, data=payload)
   if response.status_code == requests.codes.ok:
       dictionary=response.json()
       del response
       # Начинаем анализ того, что получили
       if dictionary["Result"]:
           # нам уже доступна структура данных ответа. Если хотите, напечатайте ее.
           # print ("Структура ответа ", dictionary.keys())
           if 'calls' in dictionary.keys():
               # нам уже доступна структура данных самого звонка. Если хотите, напечатайте ее.
               # print ("Структура звонков ", dictionary["calls"][1].keys())
               # print ("Структура [1] ", dictionary["calls"][1])
               # Далее запуск массового многопоточного скачивания записей всех полученых звонков.
               pool.map(create_MP3file, dictionary["calls"])
               pool.close()
               pool.join()
           else:
               print ("Результат нормальный, но Нет звонков")
       else:
           print ("Что-то пошло не так. Плохой результат получили ", dictionary["Result"])
   else:
       print ("Совсем плохо. Получили код ", response.status_code)
   # Печатаем время завершения работы и выходим.
   print ("Конец исполнения: ", str(datetime.datetime.utcnow()))