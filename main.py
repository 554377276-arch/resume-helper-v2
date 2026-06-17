from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rag.retriever import retrieve
from llm import ask_llm

# =========================
# 1. FastAPI 初始化
# =========================
app = FastAPI()

# =========================
# 2. 静态文件（CSS / JS）
# =========================
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# 3. 模板引擎（Jinja2）
# =========================
templates = Jinja2Templates(directory="templates")


# =========================
# 4. 首页（ChatGPT 页面）
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# =========================
# 5. RAG + LLM 问答接口
# =========================
@app.get("/rag-qa")
def rag_qa(query: str, top_k: int = 2):

    # 1. RAG 检索
    results = retrieve(query, top_k)

    # 2. 取最高相似度，并转成普通 Python float
    best_score = float(results[0][1])

    # 3. 判断是否使用 RAG，并转成普通 Python bool
    use_rag = bool(best_score > 0.55)

    # 4. 拼接上下文
    context = "\n".join([text for text, score in results])

    # 5. 调用大模型
    answer = ask_llm(query, context, use_rag=use_rag)

    # 6. 返回 JSON
    return {
        "query": query,
        "use_rag": use_rag,
        "best_score": best_score,
        "context": context,
        "answer": answer
    }