import logging
import logging.handlers
import multiprocessing
from dotenv import dotenv_values, find_dotenv

from external_apis.coingecko import CoinGecko
from external_apis.marketdata import MarketData
from external_apis.coinapi import CoinAPI

from db.mongo_interface import MongoInterface

from jobs import PriceDataJobs

# Load environment variables
config = dotenv_values(dotenv_path=find_dotenv())


def live_price_worker():
    # Configurations for jobs
    job_configs = [
        {
            "job_type": "live_price",
            "api_handler": CoinGecko(),
            "api_name": "coingecko",
            "params": {"BTC": {"asset_name": "bitcoin", "vs_currency": "usd", "collection_name": "btc_live_price"},
                       "ETH": {"asset_name": "ethereum", "vs_currency": "usd", "collection_name": "eth_live_price"}
                       }
        }
    ]

    mongo_handler = MongoInterface(db_name=config['MONGO_DB_NAME'],
                                   connection_url=config['MONGO_DB_CONNECTION_STRING'])

    PriceDataJobs(job_configs=job_configs,
                  mongo_handler=mongo_handler).job_runner()

    return


if __name__ == '__main__':

    # process queue
    processes = []

    live_price_job_process = multiprocessing.Process(target=live_price_worker)

    live_price_job_process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()
    pass
