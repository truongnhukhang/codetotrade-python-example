from typing import Dict

import numpy
import numpy as np
from coin_algorithm.domain.chart import Chart
from coin_algorithm.domain.plot import Plot
from talib import abstract

from coin_algorithm.domain.base_bot import BaseBot
from coin_algorithm.domain.trade_metadata import TradeMetadata


class MyChartingBot(BaseBot):

    def init(self, config: Dict[str, str]) -> None:
        nd_closes = numpy.array(self.bar_series.closes, dtype=np.double)
        self.rsi = abstract.RSI(nd_closes, 14)
        self.ema34 = abstract.EMA(nd_closes, timeperiod=34)

        self.bar_series_1h = self.other_bar_series[60]
        nd_closes_1h = numpy.array(self.bar_series_1h.closes, dtype=np.double)
        self.macd, self.macdsignal, self.macdhist = abstract.MACD(nd_closes_1h, fastperiod=12, slowperiod=26,
                                                                  signalperiod=9)
        self.ema34_1h = abstract.EMA(nd_closes_1h, timeperiod=34)

        main_chart = Chart(is_overlay=True, name="Main Chart")
        main_chart.add_plot(Plot(name="ema34", color="#FFB3BA", bar_series=self.bar_series,
                                 indicator_values=numpy.nan_to_num(self.ema34).tolist()))
        main_chart.add_plot(Plot(name="ema34-1h", color="#BAFFC9", bar_series=self.bar_series_1h,
                                 indicator_values=numpy.nan_to_num(self.ema34_1h).tolist()))

        rsi_chart = Chart(is_overlay=False, name="RSI")
        rsi_chart.add_plot(Plot(name="rsi", color="#FFDFBA", bar_series=self.bar_series,
                                indicator_values=numpy.nan_to_num(self.rsi).tolist()))

        macd_chart = Chart(is_overlay=False, name="MACD")
        macd_chart.add_plot(Plot(name="MACD", color="#BAFFC9", bar_series=self.bar_series_1h,
                                 indicator_values=numpy.nan_to_num(self.macd).tolist()))
        macd_chart.add_plot(Plot(name="MACD-SIGNAL", color="#FFFFBA", bar_series=self.bar_series_1h,
                                 indicator_values=numpy.nan_to_num(self.macdsignal).tolist()))
        macd_chart.add_plot(Plot(name="MACD-HIST", color="#E6BAFF", bar_series=self.bar_series_1h,style="COLUMN",
                                 indicator_values=numpy.nan_to_num(self.macdhist).tolist()))
        self.chart_list.append(main_chart)
        self.chart_list.append(rsi_chart)
        self.chart_list.append(macd_chart)

    def is_buy(self, idx: int) -> bool:
        return False

    def is_sell(self, idx: int) -> bool:
        return False

    def buy(self, idx: int) -> TradeMetadata:
        return TradeMetadata(0, 0)

    def sell(self, idx: int) -> TradeMetadata:
        return TradeMetadata(0, 0)

    def is_close_buy_position(self, idx: int) -> bool:
        return False

    def is_close_sell_position(self, idx: int) -> bool:
        return False
