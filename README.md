# paperGPT

A retrieval-augmented generation assistant for scientific papers.

This project demonstrates:
- PDF parsing
- document chunking
- embeddings
- vector search with FAISS
- answer generation with source citations
- Streamlit deployment

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build an index

```bash
python scripts/build_index.py --pdf path/to/paper.pdf --index_dir indexes/example_paper
```

## Ask a question

```bash
python scripts/ask.py --index_dir indexes/example_paper --question "What is the main contribution of the paper?"
```

## Demo

```bash
streamlit run app/streamlit_app.py
```


