import time
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from external_apis.coingecko import CoinGecko

from utils.time_conversions import get_iso_range_from_now, convert_iso_to_timestamp

from db.schemas.price_schemas import CoinGeckoPrice, MarketDataPrice, CoinApiTimeSeriesPrice


job_configs = [
    {
        "job_type": "live_price",
        "api_handler": CoinGecko(),
        "api_name": "coingecko",
        "params": {"BTC": ["bitcoin", "usd", "btc_live_price"], "ETH": ["ethereum", "usd", "eth_live_price"]},
    }
]


class PriceDataJobs:

    def __init__(self, job_config, mongo_handler):
        """
        :param external_api_handler: Api handler class. For example CoinGecko or MarketData
        :param mongo_handler: Handler class for MongoDB
        """
        self.job_config = job_config
        self.mongo_handler = mongo_handler

    def job_runner(self, run_indefinitely=True):
        while run_indefinitely:
            for job in self.job_config:
                if job['job_type'] == 'live_price':
                    print("Running live price job...")
                    self.live_price_job(job_config=job, mongo_handler=self.mongo_handler)
                elif job['job_type'] == 'historical':
                    pass
                else:
                    raise Exception("Invalid job type")
            print("Job runner sleeping for 30 seconds...")
            time.sleep(30)

    @classmethod
    def live_price_job(cls, job_config, mongo_handler):
        """
        Get live price data from CoinGecko and MarketData apis
        :param job_config: Job config dict that contains api_handler and params needed for the job
        :param mongo_handler: Mongo handler class
        :return:
        """
        try:
            for asset in job_config['params'].keys():
                params = job_config['params'][asset]
                live_price_response = job_config['api_handler'].get_live_price(params[0], params[1])

                if live_price_response is not None:
                    # Create data objects for MONGO
                    live_price_data = None
                    if job_config['api_name'] == 'coingecko':
                        live_price_data = CoinGeckoPrice(**live_price_response)

                    # Insert data into MONGO
                    if live_price_data is not None:
                        insert_result = mongo_handler.insert(collection=params[2],
                                                             document=live_price_data.dict())
                        if insert_result.acknowledged:
                            print(f"{asset} live price data inserted successfully")
                            print("Insert result: ", insert_result)
                        else:
                            raise Exception(f"{asset} live price data insert failed")
                    else:
                        raise Exception(
                            f"Live price data object creation failed for {asset} using {job_config['api_name']}")

        except Exception as e:
            print(f"An error occurred while processing live data: {str(e)}")
            # Wait for 10 seconds before trying again
            time.sleep(10)


# TODO: Refine job. Currently CoinAPI call does not span 24 hours
def timeseries_data_job(coinapi_handler, mongo_handler):
    """
    Get timeseries price data from CoinAPI
    :param coinapi_handler: CoinAPI class
    :param mongo_handler: MarketData class
    :return:
    """

    while True:
        try:
            # Get ISO range for last 24 hours
            iso_range_dict = get_iso_range_from_now(num_hours=24)

            # Get BTC price timeseries from CoinAPI
            coinapi_ts_btc = coinapi_handler.get_price_timeseries(symbol_id='BTC',
                                                                  vs_currency='USD',
                                                                  start_time_iso=iso_range_dict['start_iso'],
                                                                  end_time_iso=iso_range_dict['end_iso'])

            # Get ETH price timeseries from CoinAPI [{},{},...]
            coinapi_ts_eth = coinapi_handler.get_price_timeseries(symbol_id='ETH',
                                                                  vs_currency='USD',
                                                                  start_time_iso=iso_range_dict['start_iso'],
                                                                  end_time_iso=iso_range_dict['end_iso'])
            if coinapi_ts_btc is not None:
                for ts_data in coinapi_ts_btc:
                    # Normalize data for insertion
                    ts_data['timestamp'] = convert_iso_to_timestamp(ts_data['time_period_start'])
                    # Create data objects for MONGO
                    btc_ts_data = CoinApiTimeSeriesPrice(**ts_data)
                    # Insert BTC data into MONGO
                    btc_insert_result = mongo_handler.insert(collection='BTC_24h_timeseries_price',
                                                             document=btc_ts_data.dict())
                    if btc_insert_result.acknowledged:
                        print("BTC price data inserted successfully")
                    else:
                        print("BTC price data insert failed")

            if coinapi_ts_eth is not None:
                for ts_data in coinapi_ts_eth:
                    # Normalize data for insertion
                    ts_data['timestamp'] = convert_iso_to_timestamp(ts_data['time_period_start'])
                    # Create data objects for MONGO
                    eth_ts_data = CoinApiTimeSeriesPrice(**ts_data)
                    # Insert ETH data into MONGO
                    eth_insert_result = mongo_handler.insert(collection='ETH_24h_timeseries_price',
                                                             document=eth_ts_data.dict())
                    if eth_insert_result.acknowledged:
                        print("ETH price data inserted successfully")
                    else:
                        print("ETH price data insert failed")

            # wait 24 hours or 86400 seconds
            print("Sleeping for 24 hours...")
            time.sleep(86400)

        except Exception as e:
            print(f"An error occurred while processing historical data: {str(e)}")
            # Wait for 10 seconds before trying again
            time.sleep(10)
    pass

