# Extractive Text Summarizer

A small, dependency-free Python project that selects the most informative sentences from an article using normalized term-frequency scoring. Selected sentences stay in their original order, making the result readable and faithful to the source.

## Features

- Rank sentences using non-stopword term frequencies.
- Choose a fixed number of sentences or a fraction of the article.
- Preserve sentence order in the summary.
- Run as a command-line tool or import `summarize()` from Python.
- Includes sample text and unit tests; no network or model/API key required.

## Setup

Python 3.10 or newer is recommended. The project uses only the Python standard library, so no third-party packages need installing.

```bash
git clone https://github.com/mohan843/extractive-text-summarizer.git
cd extractive-text-summarizer
python -m venv .venv
# Activate the virtual environment if desired
python -m pip install -r requirements.txt
```

## Usage

Summarize the included sample with three sentences:

```bash
python summarizer.py data/article.txt --sentences 3
```

Choose by fraction instead:

```bash
python summarizer.py data/article.txt --ratio 0.4
```

Use the function in your own code:

```python
from summarizer import summarize

summary = summarize("Your article goes here.", sentence_count=1)
print(summary)
```

Run tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

## How it works

The program splits input into sentences, counts non-stopword terms across the document, and scores each sentence by its average normalized term frequency. A light length penalty discourages unusually long sentences. It selects the top-ranked sentences, then restores their source order. This is an educational baseline, not a substitute for human review or a semantic neural summarizer.

## Files

- `summarizer.py`: scoring, public API, and CLI.
- `data/article.txt`: sample article for experimentation.
- `tests/test_summarizer.py`: unit tests for ranking, input validation, and edge cases.
- `requirements.txt`: documents the standard-library-only runtime.
