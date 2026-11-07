
```bash
cat << 'EOF' > README.md
# Algo Trading Engine

A minimal Python backtesting engine built with FastAPI and Pandas to run quantitative trading strategies and track risk metrics.

## Features
- **Strategy Execution**: Moving Average Crossover combined with RSI filter.
- **Risk Metrics**: Automated calculation of Sharpe Ratio and Maximum Drawdown.
- **API Interface**: REST endpoints powered by FastAPI for initiating backtests.
- **Dockerized Setup**: Ready to deploy with Docker Compose.

## Project Structure
```text
├── core/
│   ├── __init__.py
│   └── metrics.py            # Sharpe Ratio & Max Drawdown formulas
├── strategies/
│   ├── __init__.py
│   └── ma_rsi_strategy.py    # Trading logic & signal generation
├── main.py                   # FastAPI application & endpoints
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

```

Getting Started

 Using Docker (Recommended)

```bash
docker compose up --build -d

```

Once running, open your browser and navigate to `http://localhost:8000/docs` to test the API.

 Local Execution

1. Install dependencies:
```bash
pip3 install -r requirements.txt

```


2. Start the FastAPI server:
```bash
uvicorn main:app --reload

```



API Endpoints

* `GET /` - Health check endpoint.
* `POST /api/backtest` - Runs the strategy backtest and returns key metrics.
EOF

git add README.md
git commit -m "add readme"
git push origin main

```

```
