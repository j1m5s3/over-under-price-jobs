import requests
from typing import Dict, Optional, List
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(dotenv_path=find_dotenv())


class CoinGecko:
    def __init__(self, api_key=None):
        # No API key required
        self.api_key = api_key
        self.base_url: str = 'https://api.coingecko.com/api/v3/'

    def get_market_chart_range(self, coin_id: str,
                               vs_currency: str,
                               from_timestamp_unix: int, to_timestamp_unix: int
                               ) -> Optional[Dict]:
        """
        Get market chart range
        :param coin_id: bitcoin, ethereum, etc
        :param vs_currency: usd, eur, etc
        :param from_timestamp_unix: 1610000000
        :param to_timestamp_unix: 1610000000
        :return:
        """

        request_url = self.base_url + 'coins/' + coin_id + '/market_chart/range'

        params = {
            'vs_currency': vs_currency,
            'from': from_timestamp_unix,
            'to': to_timestamp_unix
        }

        try:
            response = requests.get(request_url, params=params)
            data = response.json()
            return data
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)

    def get_live_price(self, coin_id: str, vs_currency: str) -> Optional[Dict]:
        """
        Get live price
        :param coin_id: bitcoin, ethereum, etc
        :param vs_currency: usd, eur, etc
        :return:
        """

        request_url = self.base_url + 'simple/price'

        params = {
            'ids': coin_id,
            'vs_currencies': vs_currency
        }

        try:
            response = requests.get(request_url, params=params)
            print("coingecko response: ", response)
            data = response.json()
            print("coingecko response data: ", data)

            if coin_id not in data.keys():
                return None
            result = data[coin_id]
            return result
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
