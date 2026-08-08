# Math 60 Final Project: Human-AI Proof Randomness

**How Random is Human-AI Interaction? A Stochastic Model of AI-Generated Mathematical Proofs**

This repository contains the code, data, and analysis for my Math 60 (Honors Probability) final research project.

## Overview

This project studies stochastic variation in AI-generated mathematical proofs. For each theorem prompt, I sampled the same AI model five times and annotated each proof attempt by:

- proof strategy,
- mathematical correctness, and
- error type.

The main idea is to treat repeated proof attempts for a fixed theorem as samples from a theorem-conditioned probability distribution over proof strategies and correctness outcomes. I then use entropy, Bayesian reliability estimates, bootstrap comparisons, and exploratory logistic regression to study how randomness relates to reliability.

<p align="center">
  <img width="920" height="750" alt="correctness_by_batch" src="https://github.com/user-attachments/assets/b2045966-a9e6-43a1-bdfe-4cef11b3476f" />

</p>

## Research questions

1. **How much does proof strategy vary across repeated generations?**  
   I measure theorem-level strategy randomness using Shannon entropy.

2. **Does greater strategy randomness predict lower correctness?**  
   I compare correctness across low- and high-entropy theorem prompts using bootstrap resampling and exploratory regression.

3. **Are some proof strategies more reliable than others?**  
   I estimate strategy-specific correctness probabilities using empirical rates and Beta-Binomial Bayesian smoothing.

## Dataset and sampling

- **Model:** `gpt-4.1-mini`
- **Temperature:** `0.8`
- **Attempts per theorem:** `5`
- **Theorem prompts:** `20`
- **Total proof attempts:** `100`
- **Batches:** 10 elementary true theorems + 10 hard or false theorem prompts

## Key results

### 1. Proof-strategy randomness varies substantially by theorem

Some prompts produced the same strategy in all five generations, while others produced multiple distinct proof approaches. The maximum observed theorem-level entropy was approximately `1.37` bits.

<p align="center">
  <img width="1130" height="555" alt="strategy_entropy_by_theorem" src="https://github.com/user-attachments/assets/b1b6edfb-6f46-474d-b110-925b73a73861" />

</p>

### 2. Entropy alone was not a strong predictor of correctness

The low-entropy group had mean correctness `0.900`, while the high-entropy group had mean correctness `0.875`. The observed difference was only `0.025`, with a bootstrap 95% interval of `[-0.183, 0.200]`.

<p align="center">
  <img width="1065" height="690" alt="entropy_vs_correctness" src="https://github.com/user-attachments/assets/7556539e-0f3e-4aa5-93b8-12ce7b47da68" />

</p>

### 3. Proof strategy was more informative than entropy alone

Counterexample-based responses were the most reliable in this dataset, while induction-based responses were the least reliable. With a `Beta(1,1)` prior, the posterior mean reliability was approximately:

- **Counterexample:** `0.938`
- **Probabilistic:** `0.917`
- **Induction:** `0.647`

<p align="center">
  <img width="1130" height="545" alt="bayesian_reliability_by_strategy" src="https://github.com/user-attachments/assets/e02a5e0a-8791-493c-b5b9-28c93f50a6a0" />

</p>

## Methods

### Categorical strategy model

For theorem \(T_i\), each generated strategy is modeled as

```text
S_ij ~ Categorical(p_i,1, ..., p_i,K)
```

The empirical strategy probabilities are used to estimate Shannon entropy:

```text
H_i = - sum_s p_i,s log2(p_i,s)
```

### Bayesian reliability by strategy

For strategy `s`, let

```text
q_s = P(correct | strategy = s)
```

Using a `Beta(1,1)` prior and observing `c_s` correct attempts out of `n_s`, the posterior is

```text
q_s | data ~ Beta(1 + c_s, 1 + n_s - c_s)
```

with posterior mean

```text
E[q_s | data] = (1 + c_s) / (2 + n_s)
```

### Bootstrap and exploratory regression

I use a median entropy split and bootstrap the difference in mean theorem-level correctness. I also fit an exploratory logistic regression using entropy, maximum strategy share, theorem difficulty, proof length, and theorem batch as predictors.

Because the dataset contains only 100 attempts and the easy batch has perfect correctness, the regression results should be interpreted cautiously.

## Repository structure

```text
.
├── data/                     # Theorem lists, annotated proof attempts, summary CSVs
├── scripts/                  # Generation, annotation, feature extraction, analysis
├── figures/                  # Plots used in the report
│   └── readme/               # Images displayed in this README
└── math60_final_report.tex   # LaTeX report source, if included
```

## Reproducing proof generation

The OpenAI API key is **not** included in this repository. To run the generation scripts, set your own environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Then run the relevant scripts from the `scripts/` directory.

## Main takeaway

AI proof generation was random, but not structureless. Some theorem prompts consistently induced one strategy, while others produced several distinct proof paths. In this preliminary dataset, **proof strategy and theorem type were more informative for correctness than strategy entropy alone**.
