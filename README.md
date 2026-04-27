# Finance Dashboard

A clean, mobile-friendly finance dashboard built with Python and Streamlit. It
shows simulated portfolio performance, stock price tracking, allocation, and
gains/losses insights without requiring API keys or external data feeds.

## Features

- Portfolio value and cumulative return charts
- Stock price tracking for selected tickers
- Holdings allocation by ticker and sector
- Realized-style gains/losses overview with sortable metrics
- Sidebar controls for date range, benchmark, tickers, and holding sizes
- Responsive cards and tables designed for desktop and mobile screens

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app generates deterministic sample market data, so every install is ready to
run immediately.
