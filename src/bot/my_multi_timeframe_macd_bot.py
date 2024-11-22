from typing import Dict

import numpy
import numpy as np
from talib import abstract

from coin_algorithm.domain.base_bot import BaseBot
from coin_algorithm.domain.trade_metadata import TradeMetadata


class MyMultiTimeframeMacdBot(BaseBot):

    def init(self, config: Dict[str, str]) -> None:
        rsi_period = int(config['rsi'])
        nd_closes = numpy.array(self.bar_series.closes, dtype=np.double)
        self.rsi = abstract.RSI(nd_closes, rsi_period)

        self.bar_series_1h = self.other_bar_series[60]
        nd_closes_1h = numpy.array(self.bar_series_1h.closes, dtype=np.double)
        slow = int(config['slow'])
        fast = int(config['fast'])
        signal = int(config['signal'])
        self.macd, self.macdsignal, self.macdhist = abstract.MACD(nd_closes_1h, fastperiod=fast, slowperiod=slow,
                                                                  signalperiod=signal)
        self.tp = float(config.get("tp", 3))
        self.sl = float(config.get("sl", 3))

    def is_buy(self, idx: int) -> bool:
        start_time = self.bar_series.bars[idx].start_time
        idx_1h = self.get_index_of_bar_series_by_start_time(self.bar_series_1h, start_time)
        if self.macd[idx_1h] > self.macdsignal[idx_1h] and self.macd[idx_1h - 1] <= self.macdsignal[idx_1h-1]:
            if self.rsi[idx] < 70:
                return True
        return False

    def is_sell(self, idx: int) -> bool:
        start_time = self.bar_series.bars[idx].start_time
        idx_1h = self.get_index_of_bar_series_by_start_time(self.bar_series_1h, start_time)
        if self.macd[idx_1h] < self.macdsignal[idx_1h] and self.macd[idx_1h - 1] >= self.macdsignal[idx_1h-1]:
            if self.rsi[idx] > 30:
                return True
        return False

    def buy(self, idx: int) -> TradeMetadata:
        start_time = self.bar_series.bars[idx].start_time
        idx_1h = self.get_index_of_bar_series_by_start_time(self.bar_series_1h, start_time)
        current_bar = self.bar_series.bars[idx]
        btc_amount = 0.1
        return TradeMetadata(
            current_bar.close,
            btc_amount,
            take_profit_price=current_bar.close * (1 + self.tp/100),
            stop_loss_price=current_bar.close * (1 - self.sl/100),
            trade_log="MyMacdBot Buy, MACD-SIGNAL:{:.6f}-{:.6f},PREV(MACD-SIGNAL):{:.6f}-{:.6f}, RSI: {:.6f}".format(
                self.macd[idx],
                self.macdsignal[idx],
                self.macd[idx_1h - 1],
                self.macdsignal[idx_1h - 1],
                self.rsi[idx]
            )
        )

    def sell(self, idx: int) -> TradeMetadata:
        start_time = self.bar_series.bars[idx].start_time
        idx_1h = self.get_index_of_bar_series_by_start_time(self.bar_series_1h, start_time)
        current_bar = self.bar_series.bars[idx]
        btc_amount = 0.1
        return TradeMetadata(
            current_bar.close,
            btc_amount,
            take_profit_price=current_bar.close * (1 - self.tp/100),
            stop_loss_price=current_bar.close * (1 + self.sl/100),
            trade_log="MyMacdBot Sell, MACD-SIGNAL:{:.6f}-{:.6f},PREV(MACD-SIGNAL):{:.6f}-{:.6f}, RSI: {:.6f}".format(
                self.macd[idx_1h],
                self.macdsignal[idx_1h],
                self.macd[idx_1h-1],
                self.macdsignal[idx_1h-1],
                self.rsi[idx]
            )
        )

    def is_close_buy_position(self, idx: int) -> bool:
        return False

    def is_close_sell_position(self, idx: int) -> bool:
        return False
