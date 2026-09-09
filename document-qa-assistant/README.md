# Document Q&A Assistant

An independent educational portfolio project, developed with AI assistance. Uses synthetic documents only; it is not affiliated with Google, Virtusa, or any employer.

## Problem and behavior
People need to find answers buried in documents. This app breaks text into overlapping chunks, ranks them using a BM25-style keyword score, and returns the strongest evidence with filenames. Optionally, a local Ollama model writes an answer from that evidence: this is retrieval-augmented generation (RAG).

**Retrieval-only mode does not generate an answer and does not use an LLM.** The retrieval score is a ranking value, not a confidence probability. No vector database or embeddings are used in this first version.

## Start here
Install Python 3.10 or newer from https://www.python.org/downloads/. Open a terminal in this project folder. On Windows use `python` (or `py`); on macOS/Linux use `python3` if `python` is unavailable. No pip packages or API keys are needed for the first run.

```bash
python app.py "How many days of annual leave do employees receive?"
```

Output includes `mode: retrieval_only`, `answer: null`, and a first source `leave-policy.txt#chunk-1` containing `18 days`. `null` means no generated answer was requested. A sample complete output is in `examples/retrieval-output.json`.

Try another question:

```bash
python app.py "When should I submit travel expense claims?"
python app.py "Volcanic magma"
```

The last question returns `No matching evidence found in these documents.`

## Optional: generate an answer with a local LLM
Install and start Ollama using its [official quickstart](https://docs.ollama.com/quickstart). Download a local text model suitable for your laptop; model downloads need internet and storage. Run `ollama list` to see installed model names. Replace `YOUR_INSTALLED_MODEL` below with the actual name; it is a placeholder, not a model to download.

```bash
python app.py "How many days of annual leave?" --model YOUR_INSTALLED_MODEL
```

The app calls the local [Ollama generate API](https://docs.ollama.com/api/generate) with streaming disabled. Use a local model, not a cloud-tagged model, if you want inference to stay on the laptop. No provider API key is required for local inference. Model output can vary and can be incorrect; check it against the returned text. Retrieved sources are evidence candidates, not proof that every generated claim is supported.

## Files and flow
`data/*.txt` contains fictional policies. `app.py` contains chunking, ranking, and the optional model call. `test_app.py` checks key behavior.

Document loading -> 180-word chunks with 40-word overlap -> keyword ranking -> top 3 chunks -> optional LLM answer. Only top-level UTF-8 `.txt` files are supported. Use `--docs PATH` for another folder and `--top-k 2` to change how many chunks are returned.

## Validate
```bash
python -m unittest -v
```
Local retrieval and mocked model request/error tests are included. Live model generation was not exercised in the preparation environment; the mock test verifies the integration contract, not model quality.

## Limitations and next steps
Keyword matching can miss synonyms and return irrelevant chunks that share a word. There is no calibrated abstention threshold, PDF parsing, persistent index, authentication, prompt-injection guarantee, or production deployment. Small context windows may truncate long inputs. Next: evaluate semantic embeddings against this baseline, expand held-out questions, add PDF parsing, and verify generated claims against sources.

## Explain it in an interview
"This learning project retrieves relevant document excerpts first, then optionally passes them to a local model. I can inspect the excerpts and test retrieval independently of generation. The first version uses keyword ranking; semantic retrieval is a future experiment."
Use this explanation after running and understanding the code. Do not describe this demo as employer work or claim production impact.
