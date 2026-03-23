from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, KNOWLEDGE_DIR

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def load_and_chunk(directory: Path = KNOWLEDGE_DIR) -> list[dict]:
    chunks = []
    for filepath in sorted(directory.glob("*.md")):
        text = filepath.read_text(encoding="utf-8")
        source = filepath.name
        start = 0
        idx = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "source_file": source,
                    "chunk_index": idx,
                })
                idx += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True)
