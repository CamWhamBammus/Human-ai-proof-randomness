import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path("data")
INPUT_PATH = DATA_DIR / "raw_hard_proof_attempts.csv"
OUTPUT_PATH = DATA_DIR / "hard_proof_attempts_with_features.csv"


def count_words(text):
    return len(str(text).split())


def count_equation_symbols(text):
    text = str(text)
    symbols = ["=", "<", ">", "\\leq", "\\geq", "\\sum", "\\prod", "\\binom", "^", "_"]
    return sum(text.count(sym) for sym in symbols)


def contains_pattern(text, pattern):
    return bool(re.search(pattern, str(text).lower()))


def main():
    df = pd.read_csv(INPUT_PATH)

    df["proof_length_words"] = df["proof_text"].apply(count_words)
    df["num_equation_symbols"] = df["proof_text"].apply(count_equation_symbols)

    df["contains_induction"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"induction|base case|inductive hypothesis|inductive step")
    )

    df["contains_contradiction"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"contradiction|suppose not|assume for contradiction")
    )

    df["contains_contrapositive"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"contrapositive")
    )

    df["contains_bijection"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"bijection|one-to-one correspondence")
    )

    df["contains_casework"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"case|cases|case 1|case 2")
    )

    df["contains_clearly_obvious"] = df["proof_text"].apply(
        lambda x: contains_pattern(x, r"clearly|obvious|trivial|easy to see")
    )

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")
    print(df[["theorem_id", "attempt_id", "proof_length_words", "contains_induction"]].head())


if __name__ == "__main__":
    main()