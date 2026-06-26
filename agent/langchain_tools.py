# 从 LangChain 里导入 tool 装饰器
# tool = 工具装饰器
# 作用：把普通 Python 函数包装成 LangChain 能识别的 Tool
from langchain.tools import tool


# 从你原来的工具文件里导入三个手写工具
# 这里不重写工具，只复用你已经写好的 rag_tool / db_tool / llm_tool
from agent.tools import rag_tool, db_tool, llm_tool


@tool("rag_tool")
def langchain_rag_tool(query: str) -> str:
    """
    当用户问题需要查询知识库、RAG、FAISS 向量库资料时，使用这个工具。
    """
    tool_result = rag_tool(query)

    return tool_result["result"]


@tool("db_tool")
def langchain_db_tool(query: str) -> str:
    """
    当用户问题需要查询人物信息、SQLite 聊天记录、历史对话内容时，使用这个工具。
    """
    tool_result = db_tool(query)

    return tool_result["result"]


@tool("llm_tool")
def langchain_llm_tool(query: str) -> str:
    """
    当用户问题不需要 RAG，也不需要数据库，只需要大模型直接回答时，使用这个工具。
    """
    tool_result = llm_tool(query)

    return tool_result["result"]


# LangChain 工具列表
# 后面 LangChain Agent 会使用这个列表
LANGCHAIN_TOOLS = [
    langchain_rag_tool,
    langchain_db_tool,
    langchain_llm_tool,
]