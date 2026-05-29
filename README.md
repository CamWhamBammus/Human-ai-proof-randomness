# Math 60 Final Project: Human-AI Proof Randomness

This repository contains code and data for my Math 60 (Honors Probability) final research project.

## Project title

**How Random is AI Mathematical Assistance? A Stochastic Model of Human Verification in AI-Generated Proofs**

## Description

This project studies Human-AI interaction in mathematical proof generation. For each theorem prompt, an AI model was sampled five times. Each generated proof attempt was annotated by proof strategy, correctness, and error type. The analysis models proof strategy as a categorical random variable and uses entropy, Bayesian reliability estimates, bootstrap comparisons, and exploratory logistic regression to study randomness and reliability.

## Contents

- `data/`: theorem lists, annotated proof attempts, and summary CSV files
- `scripts/`: Python scripts for generation, feature extraction, annotation setup, and statistical analysis
- `figures/`: final plots used in the report
- `math60_final_report.tex`: LaTeX report source, if included

## Model and sampling

- Model: `gpt-4.1-mini`
- Temperature: `0.8`
- Attempts per theorem: `5`
- Total theorem prompts: `20`
- Total proof attempts: `100`

## Notes

The OpenAI API key is not included in this repository. To reproduce proof generation, set your own `OPENAI_API_KEY` environment variable.
