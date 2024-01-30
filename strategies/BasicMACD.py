# -------------------------------
from freqtrade.strategy import IStrategy
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta


class BasicMACD(IStrategy):


    timeframe = '5m'
    stoploss = -0.10

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        macd, macdsignal, macdhist = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe['macd'] = macd
        dataframe['macdsignal'] = macdsignal
        dataframe['macdhist'] = macdhist

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Place holder
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['close'].shift(1))
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Place holder
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['close'].shift(1))
            ),
            'enter_long'] = 1
        return dataframe