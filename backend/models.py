from uuid import uuid4
from hashlib import md5
from dataclasses import dataclass
from typing import Dict, List


@dataclass()
class DollarPrice:
    def __init__(self, price, timestamp, uid=None) -> None:
        self.price = price
        self.timestamp = timestamp
        self.uid = uid if uid else str(uuid4())
    price: int
    timestamp: int
    uid: str


@dataclass()
class DollarModel:
    current_price: DollarPrice
    historic_prices: List[DollarPrice]

@dataclass()
class CurrencyRate:
    def __init__(self, currencyCode, alias_name, rate, has_manual_rate, manual_rate, adjustment,
                 uid=None) -> None:
        self.uid = uid if uid else str(uuid4())
        self.currencyCode = currencyCode
        self.alias_name = alias_name
        self.rate = rate
        self.has_manual_rate = has_manual_rate
        self.manual_rate = manual_rate
        self.adjustment = adjustment

    currencyCode: str
    alias_name: str
    rate: float
    has_manual_rate: bool
    manual_rate: float
    adjustment: int



@dataclass()
class CurrencyModel:
    selected_currencies: List[str]
    currency_rates: List[CurrencyRate]


@dataclass()
class BotInterval:
    unit: str
    value: int


@dataclass()
class BotModel:
    disabled: bool
    onTime: bool
    onChange: bool

    interval: BotInterval


@dataclass()
class AppState:
    dollar_model: DollarModel
    currency_model: CurrencyModel
    bot_model: BotModel

    @staticmethod
    def initialize_test():
        dollar_model = DollarModel(
            current_price=DollarPrice(44000, 1679313387),
            historic_prices=[DollarPrice(44135, 1678313387)]
        )

        currency_model = CurrencyModel(
            selected_currencies=[],
            currency_rates=[
                            ]
        )

        bot_model = BotModel(disabled=False, onTime=True, onChange=False,
                             interval=BotInterval(unit='Min', value=1))
        return AppState(dollar_model, currency_model, bot_model)
