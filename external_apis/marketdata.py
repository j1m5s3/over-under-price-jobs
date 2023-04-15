import requests
from typing import Dict, Optional, List


class MarketData:
    def __init__(self, api_key):
        self.api_key: str = api_key
        self.base_url: str = 'https://api.cryptowat.ch/'

        self.headers: Dict = {
            'X-CW-API-Key': self.api_key,
        }

    def get_live_price(self, exchange: str, pair: str) -> Optional[Dict]:
        """
        Get live price
        :param exchange: kraken, coinbase, etc
        :param pair: btcusd, ethusd, etc
        :return:
        """

        request_url = self.base_url + 'markets' + '/' + exchange + '/' + pair + '/price'

        try:
            response = requests.get(request_url, headers=self.headers)
            print("marketdata response: ", response)
            data = response.json()
            print("marketdata response data: ", data)

            if 'result' not in data.keys():
                return None
            price = data['result']
            return price
        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
