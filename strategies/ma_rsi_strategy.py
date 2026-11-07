import pandas as pd
import numpy as np

class MovingAverageRSIStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50, rsi_period: int = 14):
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_period = rsi_period

    def calculate_rsi(self, series: pd.Series) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / (loss + 1e-9)
        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        data['sma_short'] = data['close'].rolling(window=self.short_window).mean()
        data['sma_long'] = data['close'].rolling(window=self.long_window).mean()
        data['rsi'] = self.calculate_rsi(data['close'])

        data['signal'] = 0
        buy_condition = (data['sma_short'] > data['sma_long']) & (data['rsi'] < 70)
        sell_condition = (data['sma_short'] < data['sma_long']) | (data['rsi'] > 70)

        data.loc[buy_condition, 'signal'] = 1
        data.loc[sell_condition, 'signal'] = -1
        
        return data
