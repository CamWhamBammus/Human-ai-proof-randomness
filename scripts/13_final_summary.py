import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

proofs = pd.read_csv(DATA_DIR / "annotated_all_proof_attempts.csv")
summary = pd.read_csv(DATA_DIR / "theorem_summary_all.csv")
strategy = pd.read_csv(DATA_DIR / "strategy_reliability_all.csv")
entropy_compare = pd.read_csv(DATA_DIR / "entropy_group_comparison.csv")

proofs["correct"] = pd.to_numeric(proofs["correct"])

print("\n=== Dataset size ===")
print(f"Total proof attempts: {len(proofs)}")
print(f"Number of theorems: {proofs['theorem_id'].nunique()}")

print("\n=== Correctness by batch ===")
print(proofs.groupby("batch")["correct"].agg(["mean", "sum", "count"]))

print("\n=== Highest entropy theorems ===")
print(summary.sort_values("strategy_entropy", ascending=False)[[
    "theorem_id", "strategy_entropy", "correct_rate", "most_common_strategy"
]].head(5))

print("\n=== Lowest entropy theorems ===")
print(summary.sort_values("strategy_entropy", ascending=True)[[
    "theorem_id", "strategy_entropy", "correct_rate", "most_common_strategy"
]].head(5))

print("\n=== Strategy reliability ===")
print(strategy[[
    "strategy", "num_attempts", "num_correct",
    "empirical_correct_rate", "posterior_mean_reliability"
]])

print("\n=== Entropy group comparison ===")
print(entropy_compare)