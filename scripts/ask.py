import argparse
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from papergpt.retriever import FaissRetriever
from papergpt.generation import answer_with_context

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index_dir", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    retriever = FaissRetriever(args.index_dir)
    retrieved = retriever.search(args.question, args.k)
    answer = answer_with_context(args.question, retrieved)
    print(answer)
    print("\nSources:")
    for i, item in enumerate(retrieved, start=1):
        print(f"[{i}] page {item['page']}, score={item['score']:.3f}")

if __name__ == "__main__":
    main()
