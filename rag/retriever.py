from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []
chunk_vectors = []


def load_knowledge():
    global chunks, chunk_vectors

    with open(
        "documents/knowledge.txt",
        "r",
        encoding="utf-8"
    ) as f:
        raw_text = f.read()

    chunks = split_to_chunks(raw_text)

    chunk_vectors = model.encode(chunks)

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
    query_vector = model.encode(query)

    scores = []

    for i, chunk_vector in enumerate(chunk_vectors):
        score = cosine_similarity(query_vector, chunk_vector)

        scores.append(
            (
                chunks[i],
                float(score)
            )
        )

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_k]


load_knowledge()