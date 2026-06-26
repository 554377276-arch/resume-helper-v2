# 导入我们刚刚封装好的正式 LangChain Agent 函数
from agent.langchain_agent import langchain_agent


# 测试 DB
result1 = langchain_agent("张三的爱好是什么？")
print("测试 1：")
print(result1)
print("=" * 50)


# 测试 RAG
result2 = langchain_agent("成都有什么好吃的？")
print("测试 2：")
print(result2)
print("=" * 50)


# 测试普通问题
result3 = langchain_agent("用一句话解释什么是 FastAPI")
print("测试 3：")
print(result3)