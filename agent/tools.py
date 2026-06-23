from llm import ask_llm
from rag.retriever import retrieve


# ================= RAG =================
def rag_tool(query):
    results = retrieve(query)

    # 把 RAG 检索出来的文本提取出来
    texts = [text for text, score in results]

    # 把多个文本合成一个字符串，方便网页显示
    answer = "\n".join(texts)

    return {
        "tool": "RAG",
        "result": answer
    }


# ================= DB =================
def db_tool(query):

    fake_db = {
        "张三": {"age": 25, "hobby": "睡觉"},
        "李四": {"age": 28, "hobby": "吃饭"},
        "王五": {"age": 30, "hobby": "睡觉+吃饭"}
    }

    for name, info in fake_db.items():
        if name in query:
            return {
                "tool": "DB",
                "result": f"{name} => {info}"
            }

    return {
        "tool": "DB",
        "result": "未找到该用户"
    }


# ================= LLM =================
def llm_tool(question, context=""):

    result = ask_llm(
        question=question,
        context=context,
        use_rag=False
    )

    return {
        "tool": "LLM",
        "result": result
    }