# -------------------------------
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class Simple(IStrategy):

    INTERFACE_VERSION: int = 3
    minimal_roi = {
        "0": 0.01
    }

    stoploss = -0.25

    timeframe = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        ema50 = ta.EMA(dataframe, timeperiod=50)
        ema200 = ta.EMA(dataframe, timeperiod=200)
        dataframe['ema50'] = ema50['ema']
        dataframe['ema200'] = ema200['ema']

        bollinger = qtpylib.bollinger_bands(dataframe['close'], window=12, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['bb_middleband'] = bollinger['mid']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                        (dataframe['macd'] > 0)  # over 0
                        & (dataframe['macd'] > dataframe['macdsignal'])  # over signal
                        & (dataframe['bb_upperband'] > dataframe['bb_upperband'].shift(1))  # pointed up
                        & (dataframe['rsi'] > 70)  # optional filter, need to investigate
                )
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 80)
            ),
            'exit_long'] = 1
        return dataframe