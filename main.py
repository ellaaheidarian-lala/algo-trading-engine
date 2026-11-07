import logging

import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from core.metrics import calculate_sharpe_ratio, calculate_max_drawdown
from strategies.ma_rsi_strategy import MovingAverageRSIStrategy

app = FastAPI(title="Algo-Trading Backtest Engine", version="1.0.0")
logger = logging.getLogger(__name__)


class BacktestResponse(BaseModel):
    status: str
    total_days: int
    final_equity: float
    sharpe_ratio: float
    max_drawdown: float


@app.get("/")
def read_root():
    return {"message": "Algorithmic Trading Engine is running successfully!"}

@app.post("/api/backtest", response_model=BacktestResponse)
def run_backtest(days: int = Query(default=100, ge=1, le=5000)):
    if days < 1 or days > 5000:
        raise HTTPException(status_code=422, detail="days must be between 1 and 5000")

    try:
        # Keep the run deterministic without changing NumPy's global RNG state.
        rng = np.random.RandomState(42)
        dates = pd.date_range(start="2026-01-01", periods=days)
        price_walk = 100 + np.cumsum(rng.randn(days) * 1.5)
        df = pd.DataFrame({"close": price_walk}, index=dates)

        strategy = MovingAverageRSIStrategy()
        result_df = strategy.generate_signals(df)

        result_df['market_returns'] = result_df['close'].pct_change()
        result_df['strategy_returns'] = result_df['market_returns'] * result_df['signal'].shift(1)
        result_df['equity_curve'] = (1 + result_df['strategy_returns'].fillna(0)).cumprod() * 10000

        sharpe = calculate_sharpe_ratio(result_df['strategy_returns'].dropna())
        mdd = calculate_max_drawdown(result_df['equity_curve'])

        return BacktestResponse(
            status="success",
            total_days=days,
            final_equity=float(result_df['equity_curve'].iloc[-1]),
            sharpe_ratio=sharpe,
            max_drawdown=mdd,
        )
    except Exception as exc:
        logger.exception("Backtest failed")
        raise HTTPException(
            status_code=500,
            detail="The backtest could not be completed.",
        ) from exc
