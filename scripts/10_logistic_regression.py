import pandas as pd
import statsmodels.api as sm
from pathlib import Path

DATA_DIR = Path("data")

PROOFS_PATH = DATA_DIR / "annotated_all_proof_attempts.csv"
SUMMARY_PATH = DATA_DIR / "theorem_summary_all.csv"


def main():
    proofs = pd.read_csv(PROOFS_PATH)
    summary = pd.read_csv(SUMMARY_PATH)

    proofs["correct"] = pd.to_numeric(proofs["correct"])
    proofs["difficulty"] = pd.to_numeric(proofs["difficulty"])
    proofs["proof_length_words"] = pd.to_numeric(proofs["proof_length_words"])

    df = proofs.merge(
        summary[["theorem_id", "strategy_entropy", "max_strategy_fraction"]],
        on="theorem_id",
        how="left"
    )

    # Convert batch to indicator: hard = 1, easy = 0
    df["is_hard"] = (df["batch"] == "hard").astype(int)

    X = df[[
        "strategy_entropy",
        "max_strategy_fraction",
        "difficulty",
        "proof_length_words",
        "is_hard"
    ]]

    X = sm.add_constant(X)
    y = df["correct"]

    model = sm.Logit(y, X)
    result = model.fit()

    print(result.summary())

    # Save coefficient table
    coef_table = pd.DataFrame({
        "coef": result.params,
        "std_err": result.bse,
        "z": result.tvalues,
        "p_value": result.pvalues,
    })

    coef_table.to_csv(DATA_DIR / "logistic_regression_results.csv")
    print("\nSaved to data/logistic_regression_results.csv")


if __name__ == "__main__":
    main()