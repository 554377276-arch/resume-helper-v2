from sentence_transformers import SentenceTransformer
import numpy as np

# =========================
# 1. 模型初始化
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# 2. 原始知识库
# =========================
raw_knowledge = [
    "FastAPI是一个高性能Web框架。FastAPI用于构建API服务。FastAPI支持异步请求。",
    "RAG是一种检索增强生成的方法。它结合检索和大模型生成。",
    "Python支持面向对象编程。Python语法简单易学。","lst是帅哥"
]

# =========================
# 3. Chunk切分函数
# =========================
def split_to_chunks(text):
    sentences = text.split("。")
    return [s.strip() for s in sentences if s.strip()]

# =========================
# 4. 构建chunk列表
# =========================
chunks = []
for doc in raw_knowledge:
    chunks.extend(split_to_chunks(doc))

# =========================
# 5. 向量化
# =========================
chunk_vectors = model.encode(chunks)

# =========================
# 6. 相似度计算
# =========================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# =========================
# 7. RAG检索（核心）
# =========================
def retrieve(query, top_k=1):

    query_vector = model.encode(query)

    scores = []

    for i, chunk_vector in enumerate(chunk_vectors):

        score = cosine_similarity(query_vector, chunk_vector)

        scores.append((chunks[i], score))

    # 按相似度排序
    scores.sort(key=lambda x: x[1], reverse=True)

    # 返回 Top-K
    return scores[:top_k]