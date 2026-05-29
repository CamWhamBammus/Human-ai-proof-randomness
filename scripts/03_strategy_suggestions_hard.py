import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
INPUT_PATH = DATA_DIR / "hard_proof_attempts_with_features.csv"
OUTPUT_PATH = DATA_DIR / "hard_proof_attempts_to_annotate.csv"


def suggest_strategy(text):
    text = str(text).lower()

    if "induction" in text or "base case" in text or "inductive hypothesis" in text:
        return "induction"

    if "contradiction" in text or "suppose not" in text or "assume for contradiction" in text:
        return "contradiction"

    if "contrapositive" in text:
        return "contrapositive"
    
    if "counterexample" in text or "not true" in text or "false" in text:
        return "counterexample"

    if "bijection" in text or "one-to-one correspondence" in text:
        return "bijection"

    if "case" in text or "cases" in text:
        return "casework"

    if "construct" in text or "define" in text:
        return "construction"

    if "count" in text or "combinatorial" in text or "choose" in text:
        return "combinatorial"

    if "probability" in text or "independent" in text or "event" in text:
        return "probabilistic"

    if "equation" in text or "simplify" in text or "rearrange" in text or "algebra" in text:
        return "algebraic"

    return "direct"


def main():
    df = pd.read_csv(INPUT_PATH)

    df["suggested_strategy"] = df["proof_text"].apply(suggest_strategy)

    df["strategy"] = ""
    df["correct"] = ""
    df["error_type"] = ""
    df["notes"] = ""

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")
    print("Now manually fill in: strategy, correct, error_type, notes")


if __name__ == "__main__":
    main()