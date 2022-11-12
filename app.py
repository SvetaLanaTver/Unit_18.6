import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Я - бот, конвертирую валюты.\n \
Чтобы начать работу, введите команду боту \
в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n \
Увидеть список всех доступных валют: /values\n \
Напомнить мои функции - команда /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы конвертировать валюту, введите команду боту \
в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n \
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ') #переводим все символы в нижний регистр и разбиваем

        if len(values) != 3:
            raise ConvertionException('Запрос не соответствует формату <валюта1> <валюта2> <количество валюты1>. \n \
Увидеть формат запроса: /help')

        quote, base, amount = values
        total_base = CryptoConverter.convert1(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        total_base = total_base * float(amount)
        text = f'Цена {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
