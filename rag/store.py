import sqlite3
import numpy as np
from config import DB_PATH


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))


def init_db():
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            source_file TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            embedding BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def clear_db():
    conn = _connect()
    conn.execute("DELETE FROM chunks")
    conn.commit()
    conn.close()


def insert_chunks(chunks: list[dict], embeddings: np.ndarray):
    conn = _connect()
    rows = [
        (c["text"], c["source_file"], c["chunk_index"], emb.tobytes())
        for c, emb in zip(chunks, embeddings)
    ]
    conn.executemany(
        "INSERT INTO chunks (text, source_file, chunk_index, embedding) VALUES (?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()


_cache = None


def get_all_embeddings() -> tuple[list[dict], np.ndarray]:
    global _cache
    if _cache is not None:
        return _cache

    conn = _connect()
    rows = conn.execute(
        "SELECT id, text, source_file, chunk_index, embedding FROM chunks"
    ).fetchall()
    conn.close()

    if not rows:
        return [], np.array([])

    chunks = [
        {"id": r[0], "text": r[1], "source_file": r[2], "chunk_index": r[3]}
        for r in rows
    ]
    dim = len(np.frombuffer(rows[0][4], dtype=np.float32))
    embeddings = np.array(
        [np.frombuffer(r[4], dtype=np.float32) for r in rows]
    )

    _cache = (chunks, embeddings)
    return _cache


def invalidate_cache():
    global _cache
    _cache = None
