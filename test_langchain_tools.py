# 从新建的 LangChain 工具包装文件中导入工具列表
from agent.langchain_tools import LANGCHAIN_TOOLS


# 查看工具数量
print("工具数量：", len(LANGCHAIN_TOOLS))


# 遍历工具列表
# item = 每一个工具
for item in LANGCHAIN_TOOLS:
    print("工具名称：", item.name)
    print("工具说明：", item.description)
    print("-" * 30)


# 测试 RAG 工具
# invoke = 调用
rag_result = LANGCHAIN_TOOLS[0].invoke({
    "query": "成都有什么好吃的？"
})

print("RAG 工具返回：")
print(rag_result)
print("=" * 50)


# 测试 DB 工具
db_result = LANGCHAIN_TOOLS[1].invoke({
    "query": "张三的爱好是什么？"
})

print("DB 工具返回：")
print(db_result)
print("=" * 50)


# 测试 LLM 工具
llm_result = LANGCHAIN_TOOLS[2].invoke({
    "query": "用一句话解释什么是 FastAPI"
})

print("LLM 工具返回：")
print(llm_result)