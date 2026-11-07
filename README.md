# Algo Trading Engine

A small FastAPI service for running a repeatable trading-strategy backtest.

The current version keeps the example intentionally focused: it generates a
synthetic daily price series, applies a moving-average crossover with an RSI
filter, builds an equity curve, and returns two useful risk metrics. It is a
good starting point for experimenting with strategies and API design; it is
not connected to a broker and it does not place live orders.

## What it does

For each backtest, the service:

1. Generates a deterministic price series with NumPy (the random seed is
   fixed, so the same number of days produces the same run).
2. Calculates 20-day and 50-day simple moving averages.
3. Calculates a 14-period RSI.
4. Creates a signal:
   - `1` when the short average is above the long average and RSI is below 70.
   - `-1` when the short average is below the long average or RSI is above 70.
   - `0` otherwise.
5. Applies the previous day's signal to daily market returns.
6. Builds an equity curve starting from 10,000.
7. Returns the final equity, annualized Sharpe ratio, and maximum drawdown.

The strategy lives in `strategies/ma_rsi_strategy.py`, while the metric
calculations are kept in `core/metrics.py`.

## Run with Docker

From the repository root:

```bash
docker compose up --build
```

The API is then available at:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Health check: <http://localhost:8000/>

Run it in the background with:

```bash
docker compose up --build -d
```

Stop the service with:

```bash
docker compose down
```

## Run locally

Python 3.11 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

On Windows PowerShell, activate the environment with:

```powershell
.venv/Scripts/Activate.ps1
```

The local server uses port `8000` by default. You can choose another port
with `uvicorn main:app --reload --port 8001`.

## API

### `GET /`

Returns a small health response:

```json
{
  "message": "Algorithmic Trading Engine is running successfully!"
}
```

### `POST /api/backtest`

Runs one backtest. The `days` query parameter is optional and defaults to
`100`.

```bash
curl -X POST "http://localhost:8000/api/backtest?days=252"
```

Example response:

```json
{
  "status": "success",
  "total_days": 252,
  "final_equity": 10234.12,
  "sharpe_ratio": 0.48,
  "max_drawdown": -0.09
}
```

The exact metric values depend on the requested number of days. The endpoint
currently generates the price data internally, so it does not accept an
uploaded CSV or a live market symbol.

## Project layout

```text
.
├── core/
│   ├── __init__.py
│   └── metrics.py              # Sharpe ratio and maximum drawdown
├── strategies/
│   ├── __init__.py
│   └── ma_rsi_strategy.py      # Moving-average + RSI signals
├── main.py                     # FastAPI app and backtest endpoint
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Metrics

- **Sharpe ratio** is annualized using 252 periods. A zero is returned when
  returns have no measurable variation.
- **Maximum drawdown** is the largest decline from a previous equity peak,
  expressed as a negative fraction. For example, `-0.15` represents a 15%
  drawdown.

## Current scope

This project is a compact backtesting example. It does not yet include
transaction costs, slippage, portfolio sizing, external market data,
authentication, persistent storage, or live order execution. Those are natural
next steps if the engine grows beyond its current demonstration purpose.
