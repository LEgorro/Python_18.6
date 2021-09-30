TOKEN = "2013943156:AAGbD_6euuLHOHM9c5CJEVCORWQXiN_7gy0"

currencies = {
    'USD': ['доллар', 'долларов', 'доллара', 'долларах', 'доллары', 'dollar', 'dollars', 'usdollar', 'usdollars', 'usd', '$'],
    'EUR': ['евро', 'euro', 'eur', '€'],
    'RUB': ['рубль', 'рублей', 'рубля', 'рублях', 'рубли', 'ruble', 'rubles', 'rub', 'rur', '₽']
}

all_values = []
for key in currencies:
    all_values += currencies.get(key)


def is_num(elem):
    try:
        float(elem.replace(',', '.'))
        amount = elem.replace(',', '.')
        return True, amount
    except ValueError:
        pass


def ends(currency, amount):
    f1 = lambda a: (a%100)//10 != 1 and a%10 == 1
    f2 = lambda a: (a%100)//10 != 1 and a%10 in [2,3,4]
    f3 = round(float(amount), 2) % 1
    if currency == 'USD':
        return 'доллар' if f1(float(amount)) else 'доллара' if (f2(float(amount)) or f3 != 0) else 'долларов'
    elif currency == 'RUB':
        return 'рубль' if f1(float(amount)) else 'рубля' if (f2(float(amount)) or f3 != 0) else 'рублей'
    elif currency == 'EUR':
        return 'евро'