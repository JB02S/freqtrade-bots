import pytest
import sys
import os
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from strategies.EMACrossover import EMACrossover
from freqtrade.strategy.interface import IStrategy


def create_data():
    data = pd.read_feather("test_data/BTC_USDT-15m.feather")
    return data

def test_ema_calculation():
    data = create_data()
    strategy = EMACrossover()
    strategy_data = strategy.populate_indicators(data)
    true_data = 
    assert

def test_signal_generation():
    data = create_data()
    strategy = EMACrossover()
    data = strategy.populate_buy_trend(data)
    data = strategy.populate_sell_trend(data)
    # Assertions to check for buy/sell signals
    return

create_data()
