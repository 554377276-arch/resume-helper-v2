# 从 LangChain OpenAI 兼容模型包里导入 ChatOpenAI
# ChatOpenAI = 聊天模型类
# DeepSeek 兼容 OpenAI 接口，所以可以用它连接 DeepSeek
from langchain_openai import ChatOpenAI
import os

# 从新版 LangChain 里导入 create_agent
# create_agent = 创建 Agent
from langchain.agents import create_agent


# 导入我们已经包装好的 LangChain 工具列表
from agent.langchain_tools import LANGCHAIN_TOOLS
from agent.agent import rewrite_query_with_history

# ================= 手动填写 DeepSeek API Key =================
# 注意：
# 1. 把 sk-xxxx 改成你的真实 DeepSeek Key
# 2. 不要上传 GitHub
# 3. 这是本地测试写法，后面再改成环境变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请先配置环境变量")

# 创建 LangChain 使用的 DeepSeek 模型
llm = ChatOpenAI(
    model="deepseek-v4-pro",
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0
)


# 创建 LangChain Agent
langchain_agent_executor = create_agent(
    model=llm,
    tools=LANGCHAIN_TOOLS,
    system_prompt="""
你是一个中文 AI 助手。

你有三个工具：

1. rag_tool
用途：查询知识库、RAG、FAISS还有护理公司向量库资料。
适合：成都美食、四川美食、旅游推荐、知识库已有资料。

2. db_tool
用途：查询人物信息。
适合：张三、李四、王五的年龄、爱好等信息。

3. llm_tool
用途：通用回答。
适合：不需要查询知识库、不需要查询人物数据库的问题。

选择规则：
- 问到张三、李四、王五，优先使用 db_tool。
- 问到成都、四川、美食、旅游推荐，优先使用 rag_tool。
- 普通概念解释，可以直接回答；如果你需要，也可以使用 llm_tool。
- 最终回答必须使用中文。
- 每次回答简单用一条消息像微信聊天一样
上下文规则：
- 如果用户当前问题里出现“他、她、这个人、那个人”，必须结合历史消息判断具体指的是谁。
- 如果历史里最近出现了张三、李四、王五，而当前问题说“他/她”，要把它理解成最近出现的那个人。
- 如果用户当前问题里出现“这里、这边、本地、附近”，必须结合历史消息判断具体地点。
- 如果历史里最近出现了成都、四川、乐山、绵阳、宜宾，而当前问题说“这里/这边”，要把它理解成最近出现的地点。
- 如果无法确定指代对象，不要乱猜，要直接说明“我不确定你指的是谁/哪里”。
"""
)


def langchain_agent(query, history=None):
    # 如果没有传入历史记录，就使用空列表
    if history is None:
        history = []

    # 先复用旧 Agent 的上下文改写函数
    # 例如：
    # query = "他几岁？"
    # history 里最近出现过 "张三"
    # final_query 就可能变成 "张三几岁？"
    final_query = rewrite_query_with_history(query, history)

    print("🧠 LangChain 原始问题：", query)
    print("🧠 LangChain 改写后问题：", final_query)

    # messages = LangChain Agent 接收的消息列表
    messages = []

    # 遍历前端传来的历史记录
    for msg in history:
        # 取出角色，例如 user / ai
        role = msg.get("role")

        # 取出消息正文
        text = msg.get("text")

        # 如果 text 为空，就跳过这一条
        if not text:
            continue

        # 前端里 AI 的角色叫 ai
        # LangChain 里助手的角色叫 assistant
        if role == "ai":
            role = "assistant"

        # 只保留 user 和 assistant 两种角色
        if role not in ["user", "assistant"]:
            continue

        # 如果最后一条历史记录就是当前问题，先不要重复加入
        if role == "user" and text == query:
            continue

        # 把历史消息加入 messages
        messages.append({
            "role": role,
            "content": text
        })

    # 注意：
    # 这里加入的不是原始 query
    # 而是改写后的 final_query
    messages.append({
        "role": "user",
        "content": final_query
    })

    # 调用 LangChain Agent
    result = langchain_agent_executor.invoke({
        "messages": messages
    })

    # 取出最后一条消息的正文
    answer = result["messages"][-1].content

    # 返回一个和旧 agent 类似的字典结构
    return {
        "tool": "LANGCHAIN_AGENT",
        "query": query,
        "final_query": final_query,
        "result": answer
    }