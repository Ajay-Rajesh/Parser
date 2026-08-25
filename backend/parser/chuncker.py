import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


KB = Path(r"backend\knowledge_base\extracted")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "। ",
        " ",
        ""
    ]
)


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)


client = chromadb.PersistentClient(
    path=r"backend\knowledge_base\vector_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def ingest_file(json_path):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    source = data["source"]

    for page in data.get("pages", []):

        text = page.get("text", "").strip()

        if not text:
            continue

        chunks = splitter.split_text(text)

        for chunk_number, chunk in enumerate(chunks):

            chunk_id = (
                f"{json_path.stem}"
                f"_p{page['page']}"
                f"_c{chunk_number}"
            )

            embedding = model.encode(chunk).tolist()

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": source,
                    "page": page["page"],
                    "chunk": chunk_number,
                    "user_uploaded": False
                }]
            )


def ingest_kb(data=None, is_user=False):

    if is_user:
        source = data["source"]

        for page in data["pages"]:
            text = page["text"].strip()
            if not text:
                continue

            chunks = splitter.split_text(text)

            for chunk_number, chunk in enumerate(chunks):
                chunk_id = (
                    f"{Path(source).stem}"
                    f"_p{page['page']}"
                    f"_c{chunk_number}"
                )

                embedding = model.encode(chunk).tolist()

                collection.add(
                    ids=[chunk_id],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{
                        "source": source,
                        "page": page["page"],
                        "chunk": chunk_number,
                        "user_uploaded": True
                    }]
                )

        print("User document vectorized.")
        return

    files = list(KB.rglob("*.json"))

    print(f"Found {len(files)} JSON files")

    for file in files:
        print(f"Ingesting: {file}")
        ingest_file(file)

    print("KB ingestion complete.")

if __name__ == "__main__":
    ingest_kb()