import telebot
from config import currencies, all_values, is_num, ends, TOKEN
from extensions import CurrenciesConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте! Это бот-конвертер валют.' \
           'Чтобы воспользоваться им, введите данные через пробел в следующем формате:\n' \
           '<название валюты>\n' \
           '<в какую валюту перевести>\n' \
           '<количество валюты>\n' \
           '\nЧтобы увидеть список доступных валют, введите команду /value'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы воспользоваться калькулятором валют, ' \
           'отправьте запрос в логически понятной форме, содержащий следующие данные:\n' \
           '- <базовая валюта, из которой надо перевести>\n' \
           '- <котируемая валюта, то есть в какую валюту перевести>\n' \
           '- <количество базовой валюты>\n' \
           'Запрос не должен содержать знаки препинания или специальные символы\n' \
           'Пример: 100 долларов в рублях\n' \
           '\nЧтобы увидеть список доступных валют, введите команду /value'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def available_currencies(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, currencies.get(key)[0]))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = message.text.replace('?', '').split(' ')
        params = []
        amount = None
        for word in text:
            if word.replace('.', '').replace(',', '').lower() in all_values:
                params.append(word.replace('.', '').replace(',', '').lower())
            elif is_num(word):
                params.append(word)
                amount = is_num(word)[1]

        index_base = None
        for i in range(len(text)):
            if is_num(text[i-1]) and text[i].replace('.', '').replace(',', '').lower() in all_values:
                index_base = i

        if len(params) == 0:
            raise APIException('Не удалось распознать запрос.\n'
                               'Проверьте правильность написания и введите запрос ещё раз.\n'
                               'Справка по программе: /help')
        elif amount is None:
            raise APIException('Не удалось распознать количество валюты.\nВведите запрос ещё раз.')
        elif len(params) == 2 and index_base is not None:
            raise APIException('Не удалось распознать конвертируемую валюту.\n'
                               'Проверьте правильность написания и введите запрос ещё раз.\n'
                               'Посмотреть список доступных валют: /value')
        elif len(params) == 2 and index_base is None:
            raise APIException('Не удалось распознать базовую валюту.\n'
                               'Проверьте правильность написания и введите запрос ещё раз.\n'
                               'Посмотреть список доступных валют: /value')
        elif len(params) == 1:
            raise APIException('Не удалось распознать валюты в запросе.\n'
                               'Проверьте правильность написания и введите запрос ещё раз.\n'
                               'Посмотреть список доступных валют: /value')
        elif len(params) > 3:
            raise APIException('Введены лишние значения.\n'
                               'Введите запрос ещё раз.\n'
                               'Справка по программе: /help')

        if params[0].replace(',', '.') == amount:
            base, quote = params[1], params[2]
        elif params[1].replace(',', '.') == amount:
            base, quote = params[2], params[0]
        elif params[2].replace(',', '.') == amount:
            base, quote = params[0], params[1]

        for key in currencies.keys():
            if base in currencies.get(key):
                base = key
            if quote in currencies.get(key):
                quote = key

        total_base = CurrenciesConverter.get_price(base, quote, amount)
        total_sum = total_base * float(amount.replace(',', '.'))

    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода пользователем.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {ends(base, amount)} это ' \
               f'{int(round(total_sum, 2)) if round(total_sum) == round(total_sum, 2) else round(total_sum, 2)} ' \
               f'{ends(quote, total_sum)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)