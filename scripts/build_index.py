import argparse
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from papergpt.pdf_utils import extract_pages
from papergpt.chunking import chunk_pages
from papergpt.retriever import FaissRetriever

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--index_dir", required=True)
    parser.add_argument("--chunk_size", type=int, default=900)
    parser.add_argument("--overlap", type=int, default=150)
    args = parser.parse_args()

    pages = extract_pages(args.pdf)
    chunks = chunk_pages(pages, args.chunk_size, args.overlap)
    FaissRetriever.build(chunks, args.index_dir)
    print(f"Indexed {len(chunks)} chunks into {args.index_dir}")

if __name__ == "__main__":
    main()
