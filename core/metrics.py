import numpy as np
import pandas as pd


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods: int = 252) -> float:
    if periods <= 0:
        raise ValueError("periods must be greater than zero")

    clean_returns = pd.to_numeric(returns, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if clean_returns.empty:
        return 0.0

    excess_returns = clean_returns - risk_free_rate / periods
    volatility = excess_returns.std()
    if not np.isfinite(volatility) or volatility == 0:
        return 0.0
    return float(np.sqrt(periods) * (excess_returns.mean() / volatility))


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    clean_equity = pd.to_numeric(equity_curve, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if clean_equity.empty:
        return 0.0

    cumulative_max = clean_equity.cummax()
    drawdown = (clean_equity - cumulative_max).div(cumulative_max.where(cumulative_max != 0))
    drawdown = drawdown.replace([np.inf, -np.inf], np.nan).dropna()
    if drawdown.empty:
        return 0.0
    return float(drawdown.min())
