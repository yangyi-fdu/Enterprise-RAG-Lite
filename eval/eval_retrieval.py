"""Retrieval evaluation: no LLM or API key needed.

Measures
  1. recall@k: does a retrieved chunk contain the answer string?
  2. the effect of chunk size and overlap on recall
  3. the relevance threshold: how many out-of-scope questions it rejects
     against how many in-scope questions it wrongly rejects

Usage (from the repository root):
    python -m eval.eval_retrieval
"""
import json
from pathlib import Path

import numpy as np

from app.config import Config
from app.retriever import Retriever, load_embedding_model

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((ROOT / "eval" / "questions.json").read_text(encoding="utf-8"))
CHUNK_CONFIGS = [(30, 0), (30, 10), (60, 0), (60, 15), (120, 0), (120, 30)]
THRESHOLDS = np.round(np.arange(0.20, 0.71, 0.05), 2)


def recall_at_k(retriever: Retriever, items: list[dict], k: int) -> float:
    found = 0
    for item in items:
        hits = retriever.search(item["q"], k)
        found += any(item["answer"] in h.text for h in hits)
    return found / len(items)


def top1_scores(retriever: Retriever, items: list[dict]) -> np.ndarray:
    return np.array([retriever.search(item["q"], 1)[0].score for item in items])


def main():
    model = load_embedding_model()
    kb = str(ROOT / Config.KNOWLEDGE_FILE)
    in_scope, cross, oos = QUESTIONS["in_scope"], QUESTIONS["cross_lingual"], QUESTIONS["out_of_scope"]
    lines = [f"# Retrieval evaluation\n",
             f"Model: `{Config.EMBEDDING_MODEL}`. {len(in_scope)} in-scope (English), "
             f"{len(cross)} cross-lingual (Korean/Chinese), {len(oos)} out-of-scope questions.\n"]

    # 1-2. Chunking ablation
    lines += ["## Chunk size and overlap\n",
              "| Chunk size (words) | Overlap | Chunks | Recall@1 | Recall@3 | Cross-lingual recall@3 |",
              "|---:|---:|---:|---:|---:|---:|"]
    for size, overlap in CHUNK_CONFIGS:
        r = Retriever.from_file(kb, model, size, overlap)
        lines.append(f"| {size} | {overlap} | {len(r.chunks)} | {recall_at_k(r, in_scope, 1):.2f} | "
                     f"{recall_at_k(r, in_scope, 3):.2f} | {recall_at_k(r, cross, 3):.2f} |")
        print(lines[-1])

    # 3. Threshold sweep on the default configuration
    r = Retriever.from_file(kb, model)
    s_in = top1_scores(r, in_scope)
    s_cross = top1_scores(r, cross)
    near = [q for q in oos if q["near_miss"]]
    far = [q for q in oos if not q["near_miss"]]
    s_near, s_far = top1_scores(r, near), top1_scores(r, far)

    lines += ["\n## Relevance threshold\n",
              f"Default chunking ({Config.CHUNK_SIZE} words, overlap {Config.CHUNK_OVERLAP}). "
              "A question falls back when its best chunk scores below the threshold.\n",
              "| Threshold | In-scope answered | Cross-lingual answered | Near-miss rejected | Off-topic rejected |",
              "|---:|---:|---:|---:|---:|"]
    for t in THRESHOLDS:
        lines.append(f"| {t:.2f} | {np.mean(s_in >= t):.2f} | {np.mean(s_cross >= t):.2f} | "
                     f"{np.mean(s_near < t):.2f} | {np.mean(s_far < t):.2f} |")
        print(lines[-1])

    lines += ["\n## Top-1 similarity by question type\n",
              "| Group | n | min | median | max |", "|---|---:|---:|---:|---:|"]
    for name, s in [("In-scope", s_in), ("Cross-lingual", s_cross),
                    ("Near-miss (out of scope)", s_near), ("Off-topic (out of scope)", s_far)]:
        lines.append(f"| {name} | {len(s)} | {s.min():.3f} | {np.median(s):.3f} | {s.max():.3f} |")

    # Questions that end up on the wrong side of the chosen threshold
    t = Config.MIN_SIMILARITY
    wrong = [(q["q"], s) for q, s in zip(in_scope + cross, np.r_[s_in, s_cross]) if s < t]
    wrong += [(q["q"], s) for q, s in zip(near + far, np.r_[s_near, s_far]) if s >= t]
    lines += [f"\n## Errors at threshold {t}\n"]
    lines += [f"- {s:.3f}  {q}" for q, s in wrong] or ["None."]

    (ROOT / "eval" / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    plot(s_in, s_cross, s_near, s_far, t)
    print("\nWrote eval/results.md and assets/score_distribution.png")


def plot(s_in, s_cross, s_near, s_far, threshold):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=150)
    groups = [("In-scope (EN)", s_in, "#1f6feb"), ("In-scope (KO/ZH)", s_cross, "#58a6ff"),
              ("Out-of-scope, near miss", s_near, "#d29922"), ("Out-of-scope, off-topic", s_far, "#cf222e")]
    for y, (name, s, color) in enumerate(groups):
        jitter = np.random.default_rng(0).uniform(-0.15, 0.15, len(s))
        ax.scatter(s, y + jitter, s=18, color=color, alpha=0.8)
    ax.axvline(threshold, color="black", linestyle="--", linewidth=1)
    ax.text(threshold + 0.005, len(groups) - 0.55, f"threshold {threshold}", fontsize=8)
    ax.set_yticks(range(len(groups)), [g[0] for g in groups], fontsize=8)
    ax.set_xlabel("Cosine similarity of the best-matching chunk", fontsize=9)
    ax.invert_yaxis()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = ROOT / "assets" / "score_distribution.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out)


if __name__ == "__main__":
    main()
