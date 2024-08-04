from telegram.ext import Updater
TOKEN = '6986229893:AAECo1MtXZLFZDJo8v2FB_8YZVsfPctRNQ4'
# получаем экземпляр `Updater`
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher
