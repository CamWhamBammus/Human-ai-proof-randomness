import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

EASY_PATH = DATA_DIR / "annotated_proof_attempts.csv"
HARD_PATH = DATA_DIR / "annotated_hard_proof_attempts.csv"
OUTPUT_PATH = DATA_DIR / "annotated_all_proof_attempts.csv"


def main():
    easy = pd.read_csv(EASY_PATH)
    hard = pd.read_csv(HARD_PATH)

    easy["batch"] = "easy"
    hard["batch"] = "hard"

    combined = pd.concat([easy, hard], ignore_index=True)

    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"Easy rows: {len(easy)}")
    print(f"Hard rows: {len(hard)}")
    print(f"Combined rows: {len(combined)}")
    print(f"Saved to {OUTPUT_PATH}")

    print("\nCorrectness counts:")
    print(combined["correct"].value_counts())


if __name__ == "__main__":
    main()