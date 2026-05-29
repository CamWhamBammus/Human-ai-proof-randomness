import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
INPUT_PATH = DATA_DIR / "annotated_proof_attempts.csv"
OUTPUT_PATH = DATA_DIR / "theorem_summary.csv"


def entropy_from_counts(counts):
    """
    Compute Shannon entropy from a vector of counts.

    H = - sum p_i log_2(p_i)
    """
    probs = counts / counts.sum()
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_PATH}. "
            "Make sure annotated_proof_attempts.csv is inside the data folder."
        )

    df = pd.read_csv(INPUT_PATH)

    # Make sure correctness is numeric
    df["correct"] = pd.to_numeric(df["correct"])

    rows = []

    for theorem_id, group in df.groupby("theorem_id"):
        strategy_counts = group["strategy"].value_counts()

        strategy_entropy = entropy_from_counts(strategy_counts)
        num_distinct_strategies = strategy_counts.size
        most_common_strategy = strategy_counts.idxmax()
        max_strategy_fraction = strategy_counts.max() / strategy_counts.sum()

        correct_rate = group["correct"].mean()
        avg_proof_length = group["proof_length_words"].mean()

        rows.append({
            "theorem_id": theorem_id,
            "theorem_text": group["theorem_text"].iloc[0],
            "subject": group["subject"].iloc[0],
            "difficulty": group["difficulty"].iloc[0],
            "num_attempts": len(group),
            "strategy_entropy": strategy_entropy,
            "num_distinct_strategies": num_distinct_strategies,
            "most_common_strategy": most_common_strategy,
            "max_strategy_fraction": max_strategy_fraction,
            "correct_rate": correct_rate,
            "avg_proof_length_words": avg_proof_length,
        })

    summary = pd.DataFrame(rows)

    summary = summary.sort_values("strategy_entropy", ascending=False)

    summary.to_csv(OUTPUT_PATH, index=False)

    print("\nTheorem-level summary:")
    print(summary[[
        "theorem_id",
        "strategy_entropy",
        "num_distinct_strategies",
        "max_strategy_fraction",
        "correct_rate",
        "most_common_strategy"
    ]])

    print(f"\nSaved summary to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()