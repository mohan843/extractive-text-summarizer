"""Lightweight extractive text summarization using sentence term frequency."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
_STOP_WORDS = set("""a an and are as at be been being but by can could did do does for from had has have he her hers him his how i if in into is it its may might more most my no not of on or our out over she should so than that the their them then there these they this those through to too up us was we were what when where which who will with would you your""".split())


def split_sentences(text: str) -> list[str]:
    \"\"\"Split text into usable sentences, tolerating blank lines and whitespace.\"\"\"
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    return [part.strip() for part in _SENTENCE_RE.split(normalized) if part.strip()]


def _terms(sentence: str) -> list[str]:
    return [word.lower() for word in _WORD_RE.findall(sentence) if word.lower() not in _STOP_WORDS]


def summarize(text: str, *, sentence_count: int = 3, ratio: float | None = None) -> str:
    \"\"\"Return the highest-scoring sentences in their original order.

    Provide either a fixed ``sentence_count`` or a ``ratio`` in (0, 1].
    Scores are normalized term frequencies, with a mild long-sentence penalty.
    \"\"\"
    if sentence_count < 1:
        raise ValueError("sentence_count must be at least 1")
    if ratio is not None and not 0 < ratio <= 1:
        raise ValueError("ratio must be greater than 0 and at most 1")
    sentences = split_sentences(text)
    if not sentences:
        return ""
    if ratio is not None:
        target = max(1, round(len(sentences) * ratio))
    else:
        target = sentence_count
    if target >= len(sentences):
        return " ".join(sentences)

    all_terms = [term for sentence in sentences for term in _terms(sentence)]
    frequencies = Counter(all_terms)
    if not frequencies:
        return " ".join(sentences[:target])
    peak = max(frequencies.values())
    weights = {term: count / peak for term, count in frequencies.items()}

    scored: list[tuple[float, int]] = []
    for index, sentence in enumerate(sentences):
        terms = _terms(sentence)
        if not terms:
            score = 0.0
        else:
            score = sum(weights[term] for term in terms) / len(terms)
            score /= 1.0 + 0.15 * max(0, len(terms) - 20)
        scored.append((score, index))

    chosen = sorted(index for _, index in sorted(scored, key=lambda pair: (-pair[0], pair[1]))[:target])
    return " ".join(sentences[index] for index in chosen)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a text file with extractive sentence ranking.")
    parser.add_argument("file", type=Path, help="UTF-8 text file to summarize")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--sentences", type=int, default=3, help="number of sentences to include (default: 3)")
    choice.add_argument("--ratio", type=float, help="fraction of sentences to include, from >0 to 1")
    args = parser.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8")
        result = summarize(text, sentence_count=args.sentences, ratio=args.ratio)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(result)


if __name__ == "__main__":
    main()
