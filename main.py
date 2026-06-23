from fastapi import FastAPI, Request,UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import init_db, create_chat, get_chats, delete_chat, add_message, get_messages
from rag.retriever import retrieve, load_knowledge
from llm import ask_llm
import shutil
from pydantic import BaseModel
from agent.agent import agent
from agent.tools import rag_tool, db_tool, llm_tool
# =========================
# 1. FastAPI 初始化
# =========================
app = FastAPI()
init_db()
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
def rag_qa(query: str,history: str = "", top_k: int = 2):
    print("当前问题:")
    print(query)

    print("聊天历史:")
    print(history)

    # 1. RAG 检索
    results = retrieve(query, top_k)

    # 2. 取最高相似度，并转成普通 Python float
    best_score = float(results[0][1])

    # 3. 判断是否使用 RAG，并转成普通 Python bool
    use_rag = bool(best_score > 0.55)

    # 4. 拼接上下文
    context = "\n".join([text for text, score in results])

    # 5. 调用大模型
    answer = ask_llm(query, context, use_rag=use_rag, history=history)

    # 6. 返回 JSON
    return {
        "query": query,
        "use_rag": use_rag,
        "best_score": best_score,
        "context": context,
        "answer": answer
    }
@app.get("/chats")
def api_get_chats():
    return {
        "chats": get_chats()
    }


@app.post("/chats")
def api_create_chat(title: str = "新对话"):
    chat_id = create_chat(title)

    return {
        "id": chat_id,
        "title": title
    }


@app.delete("/chats/{chat_id}")
def api_delete_chat(chat_id: int):
    delete_chat(chat_id)

    return {
        "message": "删除成功",
        "id": chat_id
    }
@app.post("/chats/{chat_id}/messages")
def api_add_message(chat_id: int, role: str, text: str):
    add_message(chat_id, role, text)

    return {
        "message": "保存成功",
        "chat_id": chat_id,
        "role": role,
        "text": text
    }


@app.get("/chats/{chat_id}/messages")
def api_get_messages(chat_id: int):
    return {
        "messages": get_messages(chat_id)
    }
@app.post("/upload")
def upload_file(
    file: UploadFile = File(...)
):

    with open(
        "documents/knowledge.txt",
        "ab"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    load_knowledge()

    return {
        "message": "上传成功，知识库已刷新"
    }
# ===== Agent请求模型 =====
class AgentRequest(BaseModel):
    query: str
    history: list = []


# ===== Agent接口（新增，不影响原有接口）=====
@app.post("/agent")
def run_agent(req: AgentRequest):

    result = agent(req.query, req.history)

    return {
        "query": req.query,
        "tool": result.get("tool"),
        "result": result.get("result")
    }

@app.get("/test-agent")
def test_agent(query: str):
    return agent(query)