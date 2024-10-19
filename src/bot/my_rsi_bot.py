from typing import Dict

import numpy
import numpy as np
from coin_algorithm.domain.base_bot import BaseBot
from coin_algorithm.domain.trade_metadata import TradeMetadata
from talib import abstract


class RSIBot(BaseBot):
    rsi_period: int
    tp: float
    sl: float
    rsi_indicator = None

    # This function use to init the global variable of the bot
    # example : rsi_indicator = RSIIndicator(14)
    def init(self, config: Dict[str, str]) -> None:
        self.rsi_period = int(config['rsi_period'])
        self.tp = float(config.get("tp", 1.05))
        self.sl = float(config.get("sl", 0.95))
        nd_closes = numpy.array(self.bar_series.closes, dtype=np.double)
        # ta-lib document https://github.com/TA-Lib/ta-lib-python/blob/master/docs/func_groups/momentum_indicators.md
        self.rsi_indicator = abstract.RSI(nd_closes, self.rsi_period)

    # This function use to check the condition to buy at the specific candle
    # candle_at_idx = self.bar_series.bars[idx]
    # candle_close_price_at_idx = self.bar_series.closes[idx]
    # example : if rsi_indicator.get_rsi(idx) < 30
    def is_buy(self, idx: int) -> bool:
        return bool(self.rsi_indicator[idx] < 30)

    # This function use to check the condition to sell
    # example : if rsi_indicator.get_rsi(idx) > 70
    def is_sell(self, idx: int) -> bool:
        return bool(self.rsi_indicator[idx] > 70)

    # This function use to create the metadata of the buy trade
    # TradeMetadata is a class that contain the information of the trade
    # TradeMetadata(price, quantity, take_profit_price, stop_loss_price, trade_log)
    # price is price we buy the coin
    # quantity is the amount of the coin we buy
    # take_profit_price is the price we want to take profit
    # stop_loss_price is the price we want to stop loss
    # trade_log is the log of the trade
    def buy(self, idx: int) -> TradeMetadata:
        current_bar = self.bar_series.bars[idx]
        return TradeMetadata(
            current_bar.close,
            0.1,
            take_profit_price=current_bar.close * self.tp,
            stop_loss_price=current_bar.close * self.sl,
            trade_log="RSIBot Buy, RSI: " + str(self.rsi_indicator[idx]),
        )

    # This function use to create the metadata of the sell trade
    # TradeMetadata is a class that contain the information of the trade
    # TradeMetadata(price, quantity, take_profit_price, stop_loss_price, trade_log)
    # price is price we sell the coin
    # quantity is the amount of the coin we sell
    # take_profit_price is the price we want to take profit
    # stop_loss_price is the price we want to stop loss
    # trade_log is the log of the trade
    def sell(self, idx: int) -> TradeMetadata:
        current_bar = self.bar_series.bars[idx]
        return TradeMetadata(
            current_bar.close,
            0.1,
            take_profit_price=current_bar.close * self.sl,
            stop_loss_price=current_bar.close * self.tp,
            trade_log="RSIBot Sell, RSI: " + str(self.rsi_indicator[idx])
        )

    # This function use to check the condition to close the buy position
    # this function will be called when we already have a buy position
    def is_close_buy_position(self, idx: int) -> bool:
        return False

    # This function use to check the condition to close the sell position
    # this function will be called when we already have a sell position
    def is_close_sell_position(self, idx: int) -> bool:
        return False
