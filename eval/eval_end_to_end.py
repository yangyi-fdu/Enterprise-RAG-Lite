"""End-to-end evaluation: retrieval + LLM, with the same prompt as the API.

For in-scope questions, the answer counts as correct when it contains the
expected fact (numbers are compared with thousands separators removed).
For out-of-scope questions, the system should either fall back before the
LLM call or have the LLM say that the handbook does not cover it.

Every answer is written to eval/end_to_end.md so the automatic checks can be
reviewed by hand.

Usage (from the repository root, with LLM_API_KEY in .env):
    python -m eval.eval_end_to_end
"""
import json
import logging
import re
from pathlib import Path

from app.config import Config
from app.llm_client import LLMClient
from app.main import SYSTEM_PROMPT, build_prompt
from app.retriever import Retriever, load_embedding_model

logging.getLogger("httpx").setLevel(logging.WARNING)

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((ROOT / "eval" / "questions.json").read_text(encoding="utf-8"))

REFUSAL = re.compile(
    r"don't know|do not know|not (?:mentioned|specified|covered|included|provided|stated|available|contain)"
    r"|no (?:information|details|mention)|doesn't (?:mention|specify|say|contain|include|provide)"
    r"|does not (?:mention|specify|say|contain|include|provide)|cannot (?:find|answer)|unable to",
    re.IGNORECASE,
)


def normalise(text: str) -> str:
    return re.sub(r"(?<=\d),(?=\d)", "", text).lower()


def contains_fact(answer: str, expected: str) -> bool:
    return normalise(expected) in normalise(answer)


def ask(retriever: Retriever, llm: LLMClient, question: str) -> tuple[str, bool]:
    hits = retriever.retrieve(question)
    if not hits:
        return Config.FALLBACK_ANSWER, True
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_prompt(question, [h.text for h in hits])}]
    return llm.chat(messages), False


def main():
    retriever = Retriever.from_file(str(ROOT / Config.KNOWLEDGE_FILE), load_embedding_model())
    llm = LLMClient()
    rows, groups = [], {}

    for group in ("in_scope", "cross_lingual", "out_of_scope"):
        for item in QUESTIONS[group]:
            answer, fallback = ask(retriever, llm, item["q"])
            if group == "out_of_scope":
                ok = fallback or bool(REFUSAL.search(answer))
                name = "near_miss" if item["near_miss"] else "off_topic"
            else:
                ok = any(contains_fact(answer, a) for a in [item["answer"], *item.get("accept", [])])
                name = group
            groups.setdefault(name, []).append(ok)
            rows.append((name, item["q"], answer.replace("\n", " "), fallback, ok))
            print(f"[{'ok' if ok else 'XX'}] {name:13s} {item['q']}")

    labels = {"in_scope": "In-scope, answer contains the fact",
              "cross_lingual": "Korean/Chinese, answer contains the fact",
              "near_miss": "Near miss, declined",
              "off_topic": "Off-topic, declined"}
    lines = ["# End-to-end evaluation\n",
             f"LLM: `{llm.model}`. Threshold {Config.MIN_SIMILARITY}, top-k {Config.DEFAULT_TOP_K}.\n",
             "| Group | Passed |", "|---|---:|"]
    lines += [f"| {labels[g]} | {sum(v)}/{len(v)} |" for g, v in groups.items()]
    lines += ["\n## All answers\n", "| Group | Question | Answer | Fallback | Pass |", "|---|---|---|:---:|:---:|"]
    lines += [f"| {g} | {q} | {a.replace('|', '/')} | {'yes' if f else ''} | {'yes' if ok else '**no**'} |"
              for g, q, a, f, ok in rows]
    (ROOT / "eval" / "end_to_end.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines[2:3 + len(groups) + 1]))


if __name__ == "__main__":
    main()
