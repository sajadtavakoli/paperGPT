import tempfile
from pathlib import Path
import sys
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from papergpt.pdf_utils import extract_pages
from papergpt.chunking import chunk_pages
from papergpt.retriever import FaissRetriever
from papergpt.generation import answer_with_context

st.set_page_config(page_title="paperGPT", page_icon="📄")
st.title("paperGPT")
st.write("Upload a PDF paper, build a local vector index, and ask citation-grounded questions.")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
question = st.text_input("Question", "What is the main contribution of this paper?")

if uploaded and st.button("Ask"):
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / uploaded.name
        pdf_path.write_bytes(uploaded.read())
        index_dir = Path(tmp) / "index"

        with st.spinner("Parsing and indexing PDF..."):
            pages = extract_pages(str(pdf_path))
            chunks = chunk_pages(pages)
            FaissRetriever.build(chunks, str(index_dir))
            retriever = FaissRetriever(str(index_dir))
            retrieved = retriever.search(question, k=5)

        with st.spinner("Generating answer..."):
            answer = answer_with_context(question, retrieved)
            st.write(answer)

        st.subheader("Retrieved sources")
        for i, item in enumerate(retrieved, start=1):
            st.markdown(f"**[{i}] Page {item['page']}**")
            st.write(item["text"][:700] + "...")
