import requests
import json
from  config import *

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException('Валюты одинаковые. \n \
Увидеть формат запроса: /start')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'{base} - такая валюта не обратывается.\n \
Увидеть список всех доступных валют: /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'{quote} -такая валюта не обратывается.\n \
Увидеть список всех доступных валют: /values')

        try:
            amount = float(amount)
            if float(amount) <= 0:
                raise APIException('Параметр <количество валюты1> должен быть > 0. \n \
                Введите запрос ещё раз')
        except ValueError:
            raise APIException(f'Некорректно указано количество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]]

        return total_quote

