import requests
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(dotenv_path=find_dotenv())


class CoinAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://rest.coinapi.io/v1/'
        self.headers = {
            'X-CoinAPI-Key': self.api_key
        }

    def get_live_price(self, symbol_id, vs_currency):
        """
        Get live price
        :param symbol_id: BTC, ETH, etc
        :param vs_currency: usd, eur, etc
        :return:
        """

        request_url = self.base_url + 'exchangerate' + '/' + symbol_id + '/' + vs_currency

        try:
            response = requests.get(request_url, headers=self.headers)
            data = response.json()
            return data
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)

    def get_price_timeseries(self, symbol_id, vs_currency, start_time_iso, end_time_iso):
        """
        Get price timeseries
        :param symbol_id: BTC, ETH, etc
        :param vs_currency: usd, eur, etc
        :param start_time_iso: 2021-01-01T00:00:00
        :param end_time_iso: 2021-01-01T00:00:00
        :return:
        """
        # https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1MIN&time_start=2023-03-13T01:00:35&time_end=2023-03-14T01:00:35
        request_url = self.base_url + 'exchangerate' + '/' + symbol_id + '/' + vs_currency + '/history'

        params = {
            'period_id': '1HRS',
            'time_start': start_time_iso,
            'time_end': end_time_iso
        }

        try:
            response = requests.get(request_url, params=params, headers=self.headers)
            data = response.json()

            if not data:
                return None

            return data
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
