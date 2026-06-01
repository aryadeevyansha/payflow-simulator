# payflow-simulator
# PayFlow Simulator

Async fintech observability platform for simulating and analyzing payment failure patterns using Python asyncio, pandas analytics, and Streamlit.

---

## Problem Statement

Payment failures in checkout systems are often silent conversion killers.

This project simulates concurrent payment traffic and analyzes:
- payment-method-wise failure rates
- retry recovery patterns
- latency percentiles
- partner-level reliability
- failure root causes

---

## Features
- Rzorpay API integration using Test keys 
- Async concurrent payment simulation using asyncio
- Retry engine for recoverable failures
- Structured JSON logging
- Pandas analytics pipeline
- Streamlit observability dashboard
- Failure analysis by payment method and partner
- Latency monitoring (p50 / p95 / p99)

---

## Tech Stack

- Python
- asyncio
- pandas
- Streamlit
- Plotly
- httpx
- Git & GitHub

---

## System Flow

Client Request → Async Simulator → Payment Response → Structured Logs → Analytics Engine → Dashboard

---

## Dashboard Preview

![Dashboard](assets/dashboard.png)

---

## Analytics Engine Output

![Analytics](assets/analytics.png)

---

## Run Locally

### Install dependencies

```bash
pip install pandas numpy streamlit plotly httpx
```

### Run simulator

```bash
python simulator/payment_driver.py
```

### Run analytics

```bash
python analytics/analytics_engine.py
```

### Run dashboard

```bash
streamlit run dashboard/app.py
```

---

## Key Learnings

- High-concurrency async workflows
- Observability metrics
- Retry engineering
- Payment-system failure analysis
- Structured logging pipelines
- Latency monitoring

---

## Future Improvements

- ML-based failure prediction
- Real-time alerting
- Partner SLA monitoring.
