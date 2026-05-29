import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
SUMMARY_PATH = DATA_DIR / "theorem_summary_all.csv"
OUTPUT_PATH = DATA_DIR / "entropy_group_comparison.csv"


def bootstrap_difference(low_values, high_values, B=5000, seed=60):
    rng = np.random.default_rng(seed)

    low_values = np.array(low_values)
    high_values = np.array(high_values)

    diffs = []

    for _ in range(B):
        low_sample = rng.choice(low_values, size=len(low_values), replace=True)
        high_sample = rng.choice(high_values, size=len(high_values), replace=True)

        diffs.append(low_sample.mean() - high_sample.mean())

    return np.percentile(diffs, [2.5, 50, 97.5])


def main():
    df = pd.read_csv(SUMMARY_PATH)

    median_entropy = df["strategy_entropy"].median()

    df["entropy_group"] = np.where(
        df["strategy_entropy"] <= median_entropy,
        "low_entropy",
        "high_entropy"
    )

    low = df[df["entropy_group"] == "low_entropy"]["correct_rate"]
    high = df[df["entropy_group"] == "high_entropy"]["correct_rate"]

    ci = bootstrap_difference(low, high)

    result = pd.DataFrame({
        "median_entropy": [median_entropy],
        "low_entropy_mean_correct_rate": [low.mean()],
        "high_entropy_mean_correct_rate": [high.mean()],
        "difference_low_minus_high": [low.mean() - high.mean()],
        "bootstrap_ci_lower": [ci[0]],
        "bootstrap_ci_median": [ci[1]],
        "bootstrap_ci_upper": [ci[2]],
    })

    result.to_csv(OUTPUT_PATH, index=False)

    print(result)
    print(f"\nSaved to {OUTPUT_PATH}")

    print("\nTheorem groups:")
    print(df[[
        "theorem_id",
        "strategy_entropy",
        "correct_rate",
        "entropy_group"
    ]])


if __name__ == "__main__":
    main()