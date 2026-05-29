import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

SUMMARY_PATH = DATA_DIR / "theorem_summary_all.csv"
STRATEGY_PATH = DATA_DIR / "strategy_reliability_all.csv"
PROOFS_PATH = DATA_DIR / "annotated_all_proof_attempts.csv"


def plot_entropy_by_theorem():
    df = pd.read_csv(SUMMARY_PATH)

    plt.figure(figsize=(10, 5))
    plt.bar(df["theorem_id"].astype(str), df["strategy_entropy"])
    plt.xlabel("Theorem ID")
    plt.ylabel("Proof-Strategy Entropy")
    plt.title("Proof-Strategy Entropy by Theorem")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "final_entropy_by_theorem.png", dpi=300)
    plt.close()


def plot_entropy_vs_correctness():
    df = pd.read_csv(SUMMARY_PATH)

    plt.figure(figsize=(7, 5))
    plt.scatter(df["strategy_entropy"], df["correct_rate"])

    for _, row in df.iterrows():
        plt.annotate(
            str(row["theorem_id"]),
            (row["strategy_entropy"], row["correct_rate"]),
            fontsize=8
        )

    plt.xlabel("Proof-Strategy Entropy")
    plt.ylabel("Correctness Rate")
    plt.title("Entropy vs. Correctness Rate by Theorem")
    plt.ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "final_entropy_vs_correctness.png", dpi=300)
    plt.close()


def plot_strategy_reliability():
    df = pd.read_csv(STRATEGY_PATH)

    plt.figure(figsize=(10, 5))
    plt.bar(df["strategy"], df["posterior_mean_reliability"])
    plt.xlabel("Proof Strategy")
    plt.ylabel("Posterior Mean Reliability")
    plt.title("Bayesian Reliability Estimate by Proof Strategy")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "final_strategy_reliability.png", dpi=300)
    plt.close()


def plot_correctness_by_batch():
    df = pd.read_csv(PROOFS_PATH)
    df["correct"] = pd.to_numeric(df["correct"])

    rates = df.groupby("batch")["correct"].mean()

    plt.figure(figsize=(6, 5))
    plt.bar(rates.index, rates.values)
    plt.xlabel("Batch")
    plt.ylabel("Correctness Rate")
    plt.title("Correctness Rate by Batch")
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "final_correctness_by_batch.png", dpi=300)
    plt.close()


def plot_error_types():
    df = pd.read_csv(PROOFS_PATH)

    errors = df["error_type"].value_counts()

    plt.figure(figsize=(10, 5))
    plt.bar(errors.index, errors.values)
    plt.xlabel("Error Type")
    plt.ylabel("Frequency")
    plt.title("Distribution of Error Types")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "final_error_types.png", dpi=300)
    plt.close()


def main():
    plot_entropy_by_theorem()
    plot_entropy_vs_correctness()
    plot_strategy_reliability()
    plot_correctness_by_batch()
    plot_error_types()

    print("Saved final figures to figures/")


if __name__ == "__main__":
    main()