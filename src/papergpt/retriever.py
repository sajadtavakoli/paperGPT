import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class FaissRetriever:
    def __init__(self, index_dir: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.index_dir = Path(index_dir)
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(str(self.index_dir / "index.faiss"))
        self.chunks = json.loads((self.index_dir / "chunks.json").read_text())

    @staticmethod
    def build(chunks, index_dir: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        index_dir = Path(index_dir)
        index_dir.mkdir(parents=True, exist_ok=True)
        model = SentenceTransformer(model_name)
        embeddings = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
        embeddings = np.asarray(embeddings, dtype="float32")
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, str(index_dir / "index.faiss"))
        (index_dir / "chunks.json").write_text(json.dumps(chunks, indent=2))

    def search(self, query: str, k: int = 5):
        q = self.model.encode([query], normalize_embeddings=True)
        scores, ids = self.index.search(np.asarray(q, dtype="float32"), k)
        return [{**self.chunks[i], "score": float(scores[0][j])} for j, i in enumerate(ids[0]) if i != -1]
