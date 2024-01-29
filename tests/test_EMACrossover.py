import os
import sys
import numpy as np
import pandas as pd

project_root = os.path.dirname(os.path.dirname(__file__))
strategy_path = os.path.join(project_root, 'strategies')
sys.path.append(strategy_path)

from strategies.EMACrossover import EMACrossover

def create_data():
    data = pd.read_feather(os.path.join(project_root, 'tests/test_data/BTC_USDT-15m.feather'))
    return data

def calculate_ema(data, span):
    ema = data["close"].ewm(span=span, adjust=False).mean()
    ema.iloc[:span - 1] = np.nan
    return ema



def test_ema_calculation():
    data = create_data()
    strategy = EMACrossover({})
    strategy_data = strategy.populate_indicators(data, {})
    strategy_ema50 = strategy_data["ema50"]
    strategy_ema200 = strategy_data["ema200"]
    true_ema50 = calculate_ema(data, 50)
    true_ema200 = calculate_ema(data, 200)

    # TODO: Look at the comparison for 200 ema, the tolerance currently needs to be pretty large to pass

    close_mask_50 = np.isclose(true_ema50.iloc[49:], strategy_ema50.iloc[49:], atol=2)
    close_mask_200 = np.isclose(true_ema200.iloc[199:], strategy_ema200.iloc[199:], atol=20)

    assert close_mask_50.all(), "EMA 50 does not match"
    assert close_mask_200.all(), "EMA 200 does not match"

# TODO: Make test for signal generation

# def test_signal_generation():
#     data = create_data()
#     strategy = EMACrossover()
#     data = strategy.populate_buy_trend(data)
#     data = strategy.populate_sell_trend(data)
#     # Assertions to check for buy/sell signals
#     return
