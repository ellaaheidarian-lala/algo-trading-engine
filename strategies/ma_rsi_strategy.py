import pandas as pd

class MovingAverageRSIStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50, rsi_period: int = 14):
        if short_window <= 0 or long_window <= 0 or rsi_period <= 0:
            raise ValueError("window and period values must be greater than zero")
        if short_window >= long_window:
            raise ValueError("short_window must be smaller than long_window")

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
        if "close" not in df.columns:
            raise ValueError("input data must contain a 'close' column")

        data = df.copy()
        data["close"] = pd.to_numeric(data["close"], errors="coerce")
        if data["close"].isna().all():
            raise ValueError("'close' must contain at least one numeric value")

        data['sma_short'] = data['close'].rolling(window=self.short_window).mean()
        data['sma_long'] = data['close'].rolling(window=self.long_window).mean()
        data['rsi'] = self.calculate_rsi(data['close'])

        data['signal'] = 0
        buy_condition = (data['sma_short'] > data['sma_long']) & (data['rsi'] < 70)
        sell_condition = (data['sma_short'] < data['sma_long']) | (data['rsi'] > 70)

        data.loc[buy_condition, 'signal'] = 1
        data.loc[sell_condition, 'signal'] = -1
        
        return data
