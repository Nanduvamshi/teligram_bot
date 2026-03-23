from rag.embedder import load_and_chunk, embed_texts
from rag.store import init_db, clear_db, insert_chunks


def main():
    print("Initializing database...")
    init_db()
    clear_db()

    print("Loading and chunking knowledge documents...")
    chunks = load_and_chunk()
    print(f"Created {len(chunks)} chunks from knowledge base")

    texts = [c["text"] for c in chunks]
    print("Generating embeddings...")
    embeddings = embed_texts(texts)

    print("Storing in database...")
    insert_chunks(chunks, embeddings)
    print(f"Done! Ingested {len(chunks)} chunks into the database.")


if __name__ == "__main__":
    main()
