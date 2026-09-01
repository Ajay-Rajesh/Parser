import chromadb
from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

client = chromadb.PersistentClient(
    path=r"backend\knowledge_base\vector_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)

reranker = FlagReranker(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=False
)

def retrieve(query, k=5):
    embedding = model.encode(query).tolist()

    # Search user vectors
    user = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        where={"user_uploaded": True},
        include=["documents", "metadatas", "distances"]
    )

    # Search main KB vectors
    kb = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        where={"user_uploaded": False},
        include=["documents", "metadatas", "distances"]
    )

    merged = []

    # User results
    for doc, meta, score in zip(
        user["documents"][0],
        user["metadatas"][0],
        user["distances"][0]
    ):
        merged.append({
            "source": meta["source"],
            "page": meta["page"],
            "user_uploaded": True,
            "score": score,
            "text": doc
        })

    # KB results
    for doc, meta, score in zip(
        kb["documents"][0],
        kb["metadatas"][0],
        kb["distances"][0]
    ):
        merged.append({
            "source": meta["source"],
            "page": meta["page"],
            "user_uploaded": False,
            "score": score,
            "text": doc
        })

   


    pairs = [[query, item["text"]] for item in merged]
    scores = reranker.compute_score(pairs)

    for item, score in zip(merged, scores):
        item["rerank_score"] = score
 # Best matches first (lower distance = better)
    merged.sort(key=lambda x: x["rerank_score"], reverse=True)
    return merged[:k]

if __name__ == "__main__":
    q = input("Ask: ")

    results = retrieve(q)

    for i, chunk in enumerate(results, 1):
        print(f"\n----- Result {i} -----")
        print("Score :", round(chunk["score"], 4))
        print("User  :", chunk["user_uploaded"])
        print("Source:", chunk["source"])
        print("Page  :", chunk["page"])
        print(chunk["text"])