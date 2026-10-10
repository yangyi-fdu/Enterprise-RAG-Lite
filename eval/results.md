# Retrieval evaluation

Model: `paraphrase-multilingual-MiniLM-L12-v2`. 40 in-scope (English), 8 cross-lingual (Korean/Chinese), 20 out-of-scope questions.

## Chunk size and overlap

| Chunk size (words) | Overlap | Chunks | Recall@1 | Recall@3 | Cross-lingual recall@3 |
|---:|---:|---:|---:|---:|---:|
| 30 | 0 | 40 | 0.70 | 0.82 | 0.75 |
| 30 | 10 | 51 | 0.80 | 0.95 | 1.00 |
| 60 | 0 | 22 | 0.68 | 0.88 | 1.00 |
| 60 | 15 | 23 | 0.78 | 0.93 | 1.00 |
| 120 | 0 | 12 | 0.82 | 0.95 | 1.00 |
| 120 | 30 | 12 | 0.82 | 0.95 | 1.00 |

## Relevance threshold

Default chunking (60 words, overlap 15). A question falls back when its best chunk scores below the threshold.

| Threshold | In-scope answered | Cross-lingual answered | Near-miss rejected | Off-topic rejected |
|---:|---:|---:|---:|---:|
| 0.20 | 1.00 | 1.00 | 0.17 | 0.75 |
| 0.25 | 1.00 | 1.00 | 0.17 | 1.00 |
| 0.30 | 1.00 | 1.00 | 0.33 | 1.00 |
| 0.35 | 0.90 | 0.88 | 0.67 | 1.00 |
| 0.40 | 0.82 | 0.88 | 0.75 | 1.00 |
| 0.45 | 0.78 | 0.75 | 0.83 | 1.00 |
| 0.50 | 0.57 | 0.62 | 0.83 | 1.00 |
| 0.55 | 0.45 | 0.50 | 0.83 | 1.00 |
| 0.60 | 0.25 | 0.38 | 0.83 | 1.00 |
| 0.65 | 0.20 | 0.25 | 0.92 | 1.00 |
| 0.70 | 0.12 | 0.25 | 1.00 | 1.00 |

## Top-1 similarity by question type

| Group | n | min | median | max |
|---|---:|---:|---:|---:|
| In-scope | 40 | 0.304 | 0.524 | 0.827 |
| Cross-lingual | 8 | 0.333 | 0.550 | 0.781 |
| Near-miss (out of scope) | 12 | 0.176 | 0.333 | 0.655 |
| Off-topic (out of scope) | 8 | 0.019 | 0.138 | 0.207 |

## Errors at threshold 0.3

- 0.637  How long is parental leave?
- 0.342  Is there free parking at the Busan office?
- 0.344  What are the salary bands for senior engineers?
- 0.393  Does Halden pay for a gym membership?
- 0.409  What is the company's revenue this year?
- 0.655  How many robots has Halden sold to Germany?
- 0.306  Can I bring my dog to the office?
- 0.324  What pension scheme does the company use?
