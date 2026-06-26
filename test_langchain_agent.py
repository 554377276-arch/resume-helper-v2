# 从 LangChain OpenAI 兼容模型包里导入 ChatOpenAI
# ChatOpenAI = 聊天模型类
# 虽然名字叫 OpenAI，但 DeepSeek 兼容 OpenAI 接口，所以也可以用它
from langchain_openai import ChatOpenAI
import os

# 从新版 LangChain 里导入 create_agent
# create_agent = 创建 Agent
# Agent = 智能体，会根据用户问题决定是否调用工具
from langchain.agents import create_agent


# 导入我们包装好的 LangChain 工具列表
from agent.langchain_tools import LANGCHAIN_TOOLS


# ================= 手动填写 DeepSeek API Key =================
# 注意：
# 1. 把下面的 sk-xxxx 改成你自己的 DeepSeek Key
# 2. 不要把真实 Key 上传 GitHub
# 3. 这个写法只适合本地临时测试
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


# 创建新版 LangChain Agent
# system_prompt = 系统提示词，用来告诉 Agent 它有哪些工具、应该如何选择
agent = create_agent(
    model=llm,
    tools=LANGCHAIN_TOOLS,
    system_prompt="""
你是一个中文 AI 助手。

你有三个工具：

1. rag_tool
用途：查询知识库、RAG、FAISS 向量库资料。
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
"""
)


# ================= 测试 1：人物信息，理论上应该调用 db_tool =================
result1 = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "张三的爱好是什么？"
        }
    ]
})

print("测试 1 最终回答：")
print(result1["messages"][-1].content)
print("=" * 50)


# ================= 测试 2：美食问题，理论上应该调用 rag_tool =================
result2 = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "成都有什么好吃的？"
        }
    ]
})

print("测试 2 最终回答：")
print(result2["messages"][-1].content)
print("=" * 50)

# ================= 测试 3：普通概念问题，理论上可以直接回答 =================
result3 = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "用一句话解释什么是 FastAPI"
        }
    ]
})
print("测试 3 最终回答：")
print(result3["messages"][-1].content)