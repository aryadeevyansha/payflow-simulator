import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PayFlow Simulator", layout="wide")

st.title("💳 PayFlow Simulator Dashboard")

df = pd.read_json("data/logs.jsonl", lines=True)

# -----------------------------
# Metrics
# -----------------------------

total_transactions = len(df)

failure_rate = (
    (df["status"] == "failed").mean() * 100
)

retry_attempts = df[df["retry_attempted"] == True]

recovery_rate = 0

if len(retry_attempts) > 0:
    recovery_rate = (
        retry_attempts["recovered_after_retry"]
        .mean() * 100
    )

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "Failure Rate",
    f"{failure_rate:.2f}%"
)

col3.metric(
    "Retry Recovery Rate",
    f"{recovery_rate:.2f}%"
)

# -----------------------------
# Failure Rate by Method
# -----------------------------

st.subheader("Failure Rate by Payment Method")

failure_by_method = (
    df.groupby("method")["status"]
    .apply(lambda x: (x == "failed").mean() * 100)
    .reset_index(name="failure_rate")
)

fig1 = px.bar(
    failure_by_method,
    x="method",
    y="failure_rate",
    color="method",
    title="Payment Method Failure Rates"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Failure Rate by Partner
# -----------------------------

st.subheader("Failure Rate by Partner")

failure_by_partner = (
    df.groupby("partner")["status"]
    .apply(lambda x: (x == "failed").mean() * 100)
    .reset_index(name="failure_rate")
)

fig2 = px.bar(
    failure_by_partner,
    x="partner",
    y="failure_rate",
    color="partner",
    title="Partner Failure Rates"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Latency Distribution
# -----------------------------

st.subheader("Latency Distribution")

fig3 = px.histogram(
    df,
    x="latency_ms",
    nbins=30,
    title="Latency Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Error Breakdown
# -----------------------------

st.subheader("Error Code Breakdown")

error_counts = (
    df["error_code"]
    .value_counts()
    .reset_index()
)

error_counts.columns = [
    "error_code",
    "count"
]

fig4 = px.pie(
    error_counts,
    names="error_code",
    values="count",
    title="Failure Root Causes"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Raw Logs
# -----------------------------

st.subheader("Raw Transaction Logs")

st.dataframe(df.head(50))