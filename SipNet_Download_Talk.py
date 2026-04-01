#!/usr/bin/env python3
import shutil
import requests
import datetime as dt

# Это переменные для запроса звонков и их записей. см. описание по ссылкам ниже
# https://newapi.sipnet.ru/apidoc.pdf (Ранее https://wiki.sipnet.ru/index.php?title=API_для_интеграции_с_CRM)
# URL основной операции имеет вид https://newapi.sipnet.ru/api.php?operation=getrec& apikey=
# Определим лимит числа скачиваемых файлов. Если это Maxgetfiles=0, то файлы не скачиваются
Maxgetfiles = 10
# Это URL запроса статистики и его основные параметры
URL = 'https://newapi.sipnet.ru/api.php'
# Создадим массив с параметрами запроса.
payload = {'operation': 'calls',   # Метод который возвращает статистику звонков и ссылки на записи.
          'apikey': 'fdde2154-4ca5-4ad8-7de3-07affa5c4ca3',   # Ключ авторизации по API получить в панели администратора ВАТС.
          'showchild': '1',       # Если указан 1 то звонки выводятся и с дочерних аккаунтов.
          'D1': '01-02-2019',     # Если не правильная дата, то сегодня
          'D2': '03-02-2019',     # Если не правильная дата, то сегодня
          'format': 'json'        # Это формат возвращаемых данных. Нам очень Json понравился
          }

# Напечатаем исходные данные, на всякий случай.
print("===============================================")
print(URL)
print(payload)
print(Maxgetfiles)
print("===============================================")

# Запрашиваем статистику звонков и начинаем разбор полученного.
response= requests.post(URL, data=payload)

if response.status_code == requests.codes.ok:
   dictionary=response.json()
   # нам уже доступна структура данных ответа. Если хотите, напечатайте ее.
   # print ("Структура ответа ", dictionary.keys())

   del response
   if dictionary["status"] != 'error':
       if 'calls' in dictionary.keys():
           # нам уже доступна структура данных самого звонка. Если хотите, напечатайте ее.
           # print ("Структура звонков ", dictionary["calls"][1].keys())
           # print ("Структура [1] ", dictionary["calls"][1])
           # Далее цикл для обхода всех полученных звонков и печати отчета по ним.
           # Статистика обрабатывается от момента запроса к началу дня
           # Для вывода звонков от начала дня к текущему моменту
           # for i in dictionary["calls"]:
           for i in reversed(dictionary["calls"]):
               if 'Phone' in i.keys():
                   print ("======================================================================================================")
                   print (i["CID"], '', i["Account"], '', i['Direction'], '\n', "Дата= " , i["GMT"], "Номер= ", i["Phone"], "АОН= ", i["CLI"], "Длительность= ", i["Duration"])
               else:
                   print ("Странный звонок у него нет номера B")
               if 'URL' in i.keys():
                   # Обнаружен URL файла с записью разговора.
                   print (i["URL"])
                   # Проверяем, не исчерпан ли лимит скачивания файлов
                   if Maxgetfiles>0:
                      # Скачаем и сохраним все обнаруженные записи имя сохраненного файла состоит из cid звонка.
                       response = requests.get(i["URL"], stream=True)
                       if response.status_code == requests.codes.ok:
                           # Тут мы формируем имя файла записи разговора, данные берем из массива с описанием параметров звонка
                           FileName = str(int(dt.datetime.strptime(i["GMT"], '%d.%m.%Y %H:%M:%S').timestamp()))+"_"+i["CLI"]+"_"+i["Phone"]+"_"+i['Direction']
                           # Определяем тип скаченного файла и выбираем нужное расширение имени файла
                           if response.headers['Content-Type'] == 'audio/mpeg':
                               FileName = FileName+".mp3"
                           else:
                               FileName = FileName+".zip"
                           FileName = FileName.replace('/', '-').replace(':', '-')
                           # Сохраняем скаченный файл с нужным именем.
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
       print ("Что-то пошло не так. Плохой результат получили ")
       print ("Статус ответа ", dictionary["status"])
       print ("Ошибка ", dictionary["errorCode"], dictionary["errorMessage"])
else:
   print ("Совсем плохо. Получили код ", response.status_code)