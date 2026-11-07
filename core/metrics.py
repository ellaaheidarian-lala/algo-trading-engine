import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods: int = 252) -> float:
    excess_returns = returns - risk_free_rate / periods
    if excess_returns.std() == 0 or np.isnan(excess_returns.std()):
        return 0.0
    return float(np.sqrt(periods) * (excess_returns.mean() / excess_returns.std()))

def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    cumulative_max = equity_curve.cummax()
    drawdown = (equity_curve - cumulative_max) / cumulative_max
    return float(drawdown.min())
