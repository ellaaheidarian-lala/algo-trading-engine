import numpy as np
import pandas as pd
import pytest
from fastapi import HTTPException

from core.metrics import calculate_max_drawdown, calculate_sharpe_ratio
from main import run_backtest
from strategies.ma_rsi_strategy import MovingAverageRSIStrategy


def test_backtest_is_deterministic_for_the_same_period():
    first = run_backtest(252)
    second = run_backtest(252)

    assert first == second
    assert first.total_days == 252
    assert np.isfinite(first.final_equity)


def test_backtest_rejects_out_of_range_period():
    with pytest.raises(HTTPException, match="between 1 and 5000"):
        run_backtest(0)


def test_strategy_rejects_invalid_data():
    strategy = MovingAverageRSIStrategy()

    with pytest.raises(ValueError, match="close"):
        strategy.generate_signals(pd.DataFrame({"price": [1, 2, 3]}))


def test_metrics_handle_empty_and_flat_series():
    assert calculate_sharpe_ratio(pd.Series(dtype=float)) == 0.0
    assert calculate_sharpe_ratio(pd.Series([0.0, 0.0])) == 0.0
    assert calculate_max_drawdown(pd.Series(dtype=float)) == 0.0
    assert calculate_max_drawdown(pd.Series([100.0, 100.0])) == 0.0
