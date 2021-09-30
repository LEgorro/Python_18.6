import requests
import json


class APIException(Exception):
    pass


class CurrenciesConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')
        total_base = json.loads(r.content)[quote]

        return total_base