from typing import List, Optional
from pydantic import BaseModel, Field, Extra

from datetime import datetime


class BasePriceModel(BaseModel):
    price: Optional[float] = Field(..., description="Price of the coin")
    timestamp: Optional[float] = Field(default_factory=lambda: datetime.now().timestamp(),
                                       description="Timestamp of the price record")
    source: Optional[str] = Field(..., description="Source of the price record")

    class Config:
        extra = Extra.allow


class CoinApiPrice(BasePriceModel):
    price: float = Field(alias="rate", description="Price of the coin")
    source: str = "CoinAPI"


class CoinApiTimeSeriesPrice(BaseModel):
    price: float = Field(alias="rate_close", description="Price of the coin")
    timestamp: float = Field(..., description="Timestamp of the price record")
    source: str = "CoinAPI"

    class Config:
        extra = Extra.ignore


class CoinGeckoPrice(BasePriceModel):
    price: float = Field(alias="usd", description="Price of the coin")
    source: str = "coingecko"


class CoinMarketCapPrice(BasePriceModel):
    price: float = Field(alias='price', description="Price of the coin")
    source: str = "coinmarketcap"


class MarketDataPrice(BasePriceModel):
    price: float = Field(alias='price', description="Price of the coin")
    source: str = "marketdata"
