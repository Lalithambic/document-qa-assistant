# GenAI Portfolio Projects

Two independent learning projects covering document retrieval, local language-model generation, and evaluation. Built with Python and developed with AI assistance, using fictional sample data.

## Explore the projects

| Project | What it does | Start here |
| --- | --- | --- |
| Document Q&A Assistant | Searches text documents and optionally uses a local Llama model through Ollama to generate an answer | [Code and instructions](./document-qa-assistant/) |
| LLM Answer Evaluator | Compares saved answers with reference answers and checks retrieval source coverage | [Code and instructions](./llm-answer-evaluator/) |

## 1. Document Q&A Assistant

Example question: **How many days of annual leave do employees receive?**

The application retrieves a fictional leave policy and passes the matching evidence to a local model. A local run with `llama3.2:1b` generated an answer stating **18 days per calendar year**.

Features:

- Overlapping text chunks and BM25-style keyword ranking.
- Source filenames and retrieved excerpts for inspection.
- Retrieval-only mode that needs no model or API key.
- Optional local answer generation through Ollama.

[View a saved local model run](./document-qa-assistant/examples/local-model-demo.json).

The model did not include a source label inside the answer in the demonstrated run, although the application returned source excerpts separately. Enforcing and validating citations is a planned improvement.

## 2. LLM Answer Evaluator

Evaluates three hand-written sample records, including one deliberately incorrect answer.

| Metric | Sample result | Interpretation |
| --- | --- | --- |
| Normalized exact match | 2 of 3 records | Two answers match their references after normalization |
| Mean answer token F1 | 0.8333 | Average lexical overlap; not factual accuracy |
| Mean source recall | 0.6667 | Average fraction of expected source IDs retrieved |

[View the evaluation report](./llm-answer-evaluator/examples/evaluation-demo.json).

These results describe the bundled synthetic examples. They do not measure the Q&A assistant's model performance. A wrong answer such as `60 days` compared with `30 days` still receives partial token-overlap credit.

## Run locally

Install Python 3.10 or newer. These projects use the Python standard library, so no pip packages are required. The commands below assume your terminal starts in the folder containing both project folders. On Windows, use `python` or `py` instead of `python3` if needed.

### Search documents without a model

```bash
cd document-qa-assistant
python3 app.py "How many days of annual leave do employees receive?"
```

### Generate an answer with a local model

Install and start [Ollama](https://ollama.com/download), then run inside `document-qa-assistant`:

```bash
ollama pull llama3.2:1b
python3 app.py "How many days of annual leave do employees receive?" --model llama3.2:1b
```

### Run the evaluator

From inside `document-qa-assistant`, switch to the second project:

```bash
cd ../llm-answer-evaluator
python3 evaluate.py
```

For automated checks, run `python3 -m unittest -v` inside either project folder.

## Scope and limitations

These are educational prototypes, not production systems. Retrieval uses keywords, not semantic embeddings or a vector database. Model answers require review; the prompt alone does not guarantee correctness or resistance to malicious document instructions. The evaluator uses lexical checks, not an LLM judge or a factuality verifier.

Only synthetic data is included. These projects do not represent employer or client work.

## Planned improvements

- Evaluate the assistant's actual generated answers on a larger held-out question set.
- Improve source citation generation and validation.
- Compare semantic retrieval with the keyword baseline.
- Add a simple user interface and document parsing support.
