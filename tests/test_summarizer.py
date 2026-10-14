import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from summarizer import split_sentences, summarize


class SummarizerTests(unittest.TestCase):
    def test_sentence_split_and_whitespace(self):
        self.assertEqual(split_sentences(" First sentence.\n\nSecond one! "), ["First sentence.", "Second one!"])

    def test_selects_relevant_sentence_and_keeps_source_order(self):
        text = ("Cats are popular pets. Dogs need daily walks. Cats often enjoy warm sunny windows. "
                "Many cats purr when they feel relaxed.")
        result = summarize(text, sentence_count=2)
        self.assertEqual(result, "Cats are popular pets. Many cats purr when they feel relaxed.")

    def test_ratio_rounds_up_to_at_least_one(self):
        self.assertEqual(summarize("One. Two. Three.", ratio=0.01), "One.")

    def test_ratio_selects_expected_count(self):
        result = summarize("A. B. C. D.", ratio=0.5)
        self.assertEqual(len(split_sentences(result)), 2)

    def test_empty_input(self):
        self.assertEqual(summarize(" \n "), "")

    def test_sentence_count_larger_than_document_returns_all(self):
        self.assertEqual(summarize("First. Second.", sentence_count=8), "First. Second.")

    def test_no_content_terms_falls_back_to_source_order(self):
        self.assertEqual(summarize("And it is. But it was. Or it is.", sentence_count=2), "And it is. But it was.")

    def test_sentence_count_must_be_positive(self):
        with self.assertRaises(ValueError):
            summarize("Text.", sentence_count=0)

    def test_ratio_validation(self):
        for ratio in (0, -0.1, 1.1):
            with self.subTest(ratio=ratio), self.assertRaises(ValueError):
                summarize("Text.", ratio=ratio)

    def test_sample_cli_file_content_summarizes(self):
        sample = (ROOT / "data" / "article.txt").read_text(encoding="utf-8")
        result = summarize(sample, sentence_count=2)
        self.assertEqual(len(split_sentences(result)), 2)
        self.assertIn("trees", result.lower())


if __name__ == "__main__":
    unittest.main()
