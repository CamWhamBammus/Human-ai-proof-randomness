import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
INPUT_PATH = DATA_DIR / "annotated_all_proof_attempts.csv"
OUTPUT_PATH = DATA_DIR / "strategy_reliability_all.csv"


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_PATH}. "
            "Make sure annotated_proof_attempts.csv is inside the data folder."
        )

    df = pd.read_csv(INPUT_PATH)
    df["correct"] = pd.to_numeric(df["correct"])

    alpha = 1
    beta = 1

    rows = []

    for strategy, group in df.groupby("strategy"):
        n = len(group)
        c = int(group["correct"].sum())
        f = n - c

        empirical_rate = c / n
        posterior_mean = (alpha + c) / (alpha + beta + n)

        rows.append({
            "strategy": strategy,
            "num_attempts": n,
            "num_correct": c,
            "num_incorrect": f,
            "empirical_correct_rate": empirical_rate,
            "posterior_mean_reliability": posterior_mean,
        })

    result = pd.DataFrame(rows).sort_values(
        "posterior_mean_reliability",
        ascending=False
    )

    result.to_csv(OUTPUT_PATH, index=False)

    print("\nStrategy reliability:")
    print(result)

    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()