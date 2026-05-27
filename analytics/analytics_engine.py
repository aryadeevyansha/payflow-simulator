import pandas as pd

df = pd.read_json("data/logs.jsonl", lines=True)

print("\nTotal Transactions:")
print(len(df))

print("\nFailure Rate by Payment Method:")
failure_by_method = (
    df.groupby("method")["status"]
    .apply(lambda x: (x == "failed").mean() * 100)
)
print(failure_by_method)

print("\nFailure Rate by Partner:")
failure_by_partner = (
    df.groupby("partner")["status"]
    .apply(lambda x: (x == "failed").mean() * 100)
)
print(failure_by_partner)

print("\nLatency Percentiles:")
print("p50:", df["latency_ms"].quantile(0.50))
print("p95:", df["latency_ms"].quantile(0.95))
print("p99:", df["latency_ms"].quantile(0.99))

print("\nRetry Recovery Rate:")
retry_attempts = df[df["retry_attempted"] == True]
if len(retry_attempts) > 0:
    recovery_rate = retry_attempts["recovered_after_retry"].mean() * 100
    print(recovery_rate)
else:
    print("No retry attempts found")

print("\nError Code Breakdown:")
print(df["error_code"].value_counts())
