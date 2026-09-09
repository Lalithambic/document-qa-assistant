# LLM Answer Evaluator

A small, independent educational portfolio project developed with AI assistance. Checks saved answers and retrieval results using transparent metrics. No model calls, API keys, or pip dependencies. Sample records are hand-written synthetic examples, not measured LLM outputs.

## Why this exists
A convincing answer may still be wrong. This tool helps compare an answer with a reference and check whether retrieval found the expected documents. It complements the Document Q&A Assistant, but also runs independently.

## Run
Install Python 3.10+. Open a terminal inside this folder. On macOS/Linux use `python3` if needed; on Windows `py` can replace `python`.

```bash
python evaluate.py
python evaluate.py data/sample_runs.json --output report.json
python -m unittest -v
```

Expected sample aggregate: 3 records, exact match about 0.6667, answer token F1 about 0.8333, source recall about 0.6667. These numbers describe only the three synthetic examples. The checked output is in `examples/sample-report.json`.

## Input and metrics
Input is a JSON array. Each record needs a unique `id`, `question`, `answer`, `expected_answer`, `retrieved_sources`, and `expected_sources`. See `data/sample_runs.json` for the exact shape.

| Metric | Meaning | Limitation |
| --- | --- | --- |
| Normalized exact match | Equal token lists after lowercasing and punctuation splitting | Correct paraphrases may fail |
| Answer token F1 | Harmonic mean of shared-token precision and recall, counting duplicates | Wrong numbers can still get partial credit |
| Source recall | Fraction of expected source IDs found in retrieved source IDs | Does not penalize extra irrelevant sources or verify claims |

Empty expected source lists give `null` recall and are excluded from the recall mean. English letters and digits are the tokenizer's scope; this is not multilingual semantic evaluation. Token normalization removes punctuation, so it is not appropriate for exact code, numeric-format, or identifier correctness.

**Example:** `60 days` versus `30 days` receives token F1 0.5 because `days` overlaps, even though the answer is factually wrong. Never treat lexical similarity as proof of correctness. This tool does not detect hallucinations or replace human review.

## Use with the Q&A assistant
Run the assistant with a local model. Copy its `answer` into a new record and its `sources[].source` values into `retrieved_sources`. Write the correct reference answer yourself after checking the document, and put the supporting source IDs into `expected_sources`. Then evaluate your saved file. Retrieval-only output has no generated answer; do not label it as a model answer.

## Next experiments
Create a larger held-out question set, measure retrieval precision and recall at fixed k, add latency tracking, and use a separately validated semantic or claim-level evaluator. Keep the original lexical baseline for comparison. There is no production-quality benchmark in this starter.
