import requests
import json
from  config import *

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Валюты одинаковые. \n \
Увидеть формат запроса: /start')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'{quote} -такая валюта не обратывается.\n \
Увидеть список всех доступных валют: /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'{base} - такая валюта не обратывается.\n \
Увидеть список всех доступных валют: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректно указано количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

