import telebot
from config import keys, TOKEN
from utils import APIException, CryptoConverter

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
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ') #переводим все символы в нижний регистр и разбиваем

        if len(values) != 3:
            raise APIException('Запрос не соответствует формату <валюта1> <валюта2> <количество валюты1>. \n \
Увидеть формат запроса: /help')

        base, quote, amount = values
        amount = amount.replace(',', '.') # заменяем запятую на точку
        total_quote = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Системная ошибка. Не удалось обработать запрос - попробуйте позже ещё раз\n{e}')
    else:
        total_quote *= float(amount)
        text = f'Цена {amount} {base} = {total_quote} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()
