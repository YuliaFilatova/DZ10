import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Невозможно перевести одинаковые валюты.')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество.')

        headers = {
            "apikey": "ImoIhFq51a1z0E9uZZQ14M4hlzKm2VQ3"
        }
        payload = {}
        url = f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"
        response = requests.request("GET", url, headers=headers, data=payload)
        total_base = json.loads(response.content)['result']
        return round(total_base, 2)
