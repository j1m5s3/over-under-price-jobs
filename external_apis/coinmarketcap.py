import requests
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(dotenv_path=find_dotenv())


class CoinMarketCap:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://pro-api.coinmarketcap.com/v2/'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

    def get_latest(self, crypto_symbol):
        request_url = self.base_url + 'cryptocurrency/quotes/latest'

        params = {
            'symbol': crypto_symbol
        }

        try:
            response = requests.get(request_url, params=params, headers=self.headers)
            data = response.json()
            return data
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
