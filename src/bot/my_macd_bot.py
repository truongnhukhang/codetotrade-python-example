from typing import Dict

import numpy
import numpy as np
from talib import abstract

from coin_algorithm.domain.base_bot import BaseBot
from coin_algorithm.domain.trade_metadata import TradeMetadata


class MyMacdBot(BaseBot):
    
    def init(self, config: Dict[str, str]) -> None:
        rsi_period = int(config['rsi'])
        nd_closes = numpy.array(self.bar_series.closes, dtype=np.double)
        self.rsi = abstract.RSI(nd_closes, rsi_period)

        slow = int(config['slow'])
        fast = int(config['fast'])
        signal = int(config['signal'])
        self.macd, self.macdsignal, self.macdhist = abstract.MACD(nd_closes, fastperiod=fast, slowperiod=slow, signalperiod=signal)

    def is_buy(self, idx: int) -> bool:
        if self.macd[idx] > self.macdsignal[idx] and self.macd[idx-1] <= self.macdsignal[-1]:
            if self.rsi[idx] < 70:
                return True
        return False

    def is_sell(self, idx: int) -> bool:
        if self.macd[idx] < self.macdsignal[idx] and self.macd[idx - 1] >= self.macdsignal[-1]:
            if self.rsi[idx] > 30:
                return True
        return False

    def buy(self, idx: int) -> TradeMetadata:
        current_bar = self.bar_series.bars[idx]
        btc_amount = 0.1
        return TradeMetadata(
            current_bar.close,
            btc_amount,
            take_profit_price=current_bar.close * 1.03,
            stop_loss_price=current_bar.close * 0.98,
            trade_log="MyMacdBot Buy, MACD-SIGNAL:{:.6f}-{:.6f},PREV(MACD-SIGNAL):{:.6f}-{:.6f}, RSI: {:.6f}".format(
                self.macd[idx],
                self.macdsignal[idx],
                self.macd[idx],
                self.macdsignal[idx],
                self.rsi[idx]
                )
        )

    def sell(self, idx: int) -> TradeMetadata:
        current_bar = self.bar_series.bars[idx]
        btc_amount = 0.1
        return TradeMetadata(
            current_bar.close,
            btc_amount,
            take_profit_price=current_bar.close * 0.98,
            stop_loss_price=current_bar.close * 1.03,
            trade_log="MyMacdBot Sell, MACD-SIGNAL:{:.6f}-{:.6f},PREV(MACD-SIGNAL):{:.6f}-{:.6f}, RSI: {:.6f}".format(
                self.macd[idx],
                self.macdsignal[idx],
                self.macd[idx],
                self.macdsignal[idx],
                self.rsi[idx]
            )
        )

    def is_close_buy_position(self, idx: int) -> bool:
        return False

    def is_close_sell_position(self, idx: int) -> bool:
        return False
