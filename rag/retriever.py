import numpy as np
import ollama
from config import OLLAMA_RAG_MODEL, TOP_K
from rag.embedder import embed_texts
from rag.store import get_all_embeddings


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    chunks, embeddings = get_all_embeddings()
    if not chunks:
        return []

    query_emb = embed_texts([query])[0]
    scores = embeddings @ query_emb
    top_indices = np.argsort(scores)[-top_k:][::-1]

    results = []
    for i in top_indices:
        chunk = chunks[i].copy()
        chunk["score"] = float(scores[i])
        results.append(chunk)
    return results


def generate_answer(query: str, context_chunks: list[dict], history: list[dict] = None) -> dict:
    context = "\n\n".join(
        f"[Source: {c['source_file']}]\n{c['text']}" for c in context_chunks
    )

    messages = []

    messages.append({
        "role": "system",
        "content": (
            "You are a helpful assistant. Answer the question using ONLY the provided context. "
            "If the context doesn't contain enough information, say so honestly. "
            "Keep your answer concise and informative."
        ),
    })

    if history:
        for entry in history:
            messages.append({"role": "user", "content": entry["query"]})
            messages.append({"role": "assistant", "content": entry["answer"]})

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}",
    })

    response = ollama.chat(model=OLLAMA_RAG_MODEL, messages=messages)
    answer = response["message"]["content"]

    sources = list({c["source_file"] for c in context_chunks})

    return {"answer": answer, "sources": sources}
