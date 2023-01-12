import telebot
from config import currency, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)


#  тестовый обработчик, чтоб проверить что бот работает
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Привет! Я бот и покажу тебе актуальный курс валют.' \
           '\n- Для начала работы введите сообщение в следующем формате:' \
           '\n<имя валюты><в какую валюту перевести><количество переводимой валюты>' \
           '\nНапример: евро рубль 10' \
           '\n- Посмотреть список доступных валют через команду: /values' \
           '\n- Напомнить, что я могу через команду: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')

        if len(parameters) > 3:
            raise APIException('Слишком много параметров.')

        if len(parameters) < 3:
            raise APIException('Слишком мало параметров.')

        quote, base, amount = parameters
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Переводим {quote} в {base}.\n {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
