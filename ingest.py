
"""Read files in data/, split into chunks, embed, and save to chroma_db/."""
import shutil
import time

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
import rag_core


def load_documents():
    docs, report = [], []
    files = sorted(p for p in config.DATA_DIR.glob("*")
                   if p.suffix.lower() in (".pdf", ".txt"))
    if not files:
        raise SystemExit("No .pdf or .txt files found in data/. Add files first.")
    for path in files:
        if path.suffix.lower() == ".pdf":
            pages = PyPDFLoader(str(path)).load()
        else:
            pages = TextLoader(str(path), encoding="utf-8").load()
        chars = sum(len(p.page_content) for p in pages)
        avg = chars // max(len(pages), 1)
        flag = "  <-- WARNING: almost no text (scanned PDF?)" if avg < 100 else ""
        report.append(f"{path.name}: {len(pages)} page(s), {chars} chars{flag}")
        docs += pages
    print("\n".join(report))
    return docs


def main():
    docs = load_documents()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    ).split_documents(docs)
    print("Total chunks:", len(chunks))

    if config.DB_DIR.exists():
        try:
            shutil.rmtree(config.DB_DIR)  # rebuild fresh: no duplicates
        except PermissionError:
            raise SystemExit("Cannot delete chroma_db/. Stop the Streamlit app "
                             "(Ctrl+C in its terminal) and run ingest again.")

    db = Chroma(persist_directory=str(config.DB_DIR),
                embedding_function=rag_core.get_embeddings())
    batch_size = 40
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        for attempt in range(5):
            try:
                db.add_documents(batch)
                break
            except Exception as e:  # free-tier rate limit: wait and retry
                wait = 20 * (attempt + 1)
                print(f"Embedding error ({e}). Waiting {wait}s, retry {attempt + 1}/5")
                time.sleep(wait)
        else:
            raise SystemExit("Embedding kept failing. Check key/model/quota.")
        print(f"Embedded {min(i + batch_size, len(chunks))}/{len(chunks)}")
        time.sleep(1)
    print("Saved database to", config.DB_DIR)


if __name__ == "__main__":
    main()
