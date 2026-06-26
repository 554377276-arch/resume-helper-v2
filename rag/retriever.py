from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
os.environ["HF_HUB_OFFLINE"] = "1"
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)
chunks = []
chunk_vectors = None
index = None

def load_knowledge():
    global chunks, chunk_vectors, index

    with open(
        "documents/knowledge.txt",
        "r",
        encoding="utf-8"
    ) as f:
        raw_text = f.read()

    chunks = split_to_chunks(raw_text)

    chunk_vectors = model.encode(chunks)
    chunk_vectors = np.array(chunk_vectors).astype("float32")

    faiss.normalize_L2(chunk_vectors)

    dimension = chunk_vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(chunk_vectors)

    print("知识库已重新加载")
    print("当前chunk数量:", len(chunks))


def split_to_chunks(text):
    sentences = text.split("。")
    return [s.strip() for s in sentences if s.strip()]


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def retrieve(query, top_k=1):

    query_vector = model.encode([query])

    query_vector = np.array(query_vector).astype("float32")

    faiss.normalize_L2(query_vector)

    scores, ids = index.search(query_vector, top_k)

    results = []

    for score, chunk_id in zip(scores[0], ids[0]):

        results.append(
            (
                chunks[chunk_id],
                float(score)
            )
        )

    return results


load_knowledge()