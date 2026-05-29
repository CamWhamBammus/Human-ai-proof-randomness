from openai import OpenAI
from pathlib import Path
import pandas as pd
import time
import sys

# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = Path("data")
THEOREMS_PATH = DATA_DIR / "theorems.csv"
OUTPUT_PATH = DATA_DIR / "raw_proof_attempts.csv"

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.8
ATTEMPTS_PER_THEOREM = 5

client = OpenAI()


# -----------------------------
# Prompt template
# -----------------------------

def make_prompt(theorem_text: str) -> str:
    return f"""
Prove the following theorem rigorously.

Theorem:
{theorem_text}

Instructions:
- Give a clear mathematical proof.
- Do not skip important logical steps.
- Do not mention that you are an AI.
- End the proof clearly.
"""


# -----------------------------
# API call
# -----------------------------

def generate_proof(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=prompt,
        temperature=TEMPERATURE,
        max_output_tokens=1000,
    )
    return response.output_text


# -----------------------------
# Main script
# -----------------------------

def main():
    if not THEOREMS_PATH.exists():
        print(f"Could not find {THEOREMS_PATH}")
        print("Make sure you created data/theorems.csv first.")
        sys.exit(1)

    theorems = pd.read_csv(THEOREMS_PATH)

    rows = []

    for _, row in theorems.iterrows():
        theorem_id = row["theorem_id"]
        theorem_text = row["theorem_text"]
        subject = row["subject"]
        difficulty = row["difficulty"]

        for attempt_id in range(1, ATTEMPTS_PER_THEOREM + 1):
            print(f"Generating theorem {theorem_id}, attempt {attempt_id}...")

            prompt = make_prompt(theorem_text)

            try:
                proof_text = generate_proof(prompt)

                rows.append({
                    "theorem_id": theorem_id,
                    "attempt_id": attempt_id,
                    "theorem_text": theorem_text,
                    "subject": subject,
                    "difficulty": difficulty,
                    "model": MODEL,
                    "temperature": TEMPERATURE,
                    "prompt": prompt,
                    "proof_text": proof_text,
                })

                # Save after every proof so you do not lose progress if something crashes
                pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)

                time.sleep(1)

            except Exception as e:
                print(f"Error on theorem {theorem_id}, attempt {attempt_id}: {e}")

                rows.append({
                    "theorem_id": theorem_id,
                    "attempt_id": attempt_id,
                    "theorem_text": theorem_text,
                    "subject": subject,
                    "difficulty": difficulty,
                    "model": MODEL,
                    "temperature": TEMPERATURE,
                    "prompt": prompt,
                    "proof_text": "",
                    "error": str(e),
                })

                pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)

    print(f"Done. Saved results to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
