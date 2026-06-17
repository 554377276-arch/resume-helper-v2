
from openai import OpenAI

client = OpenAI(
    api_key="sk-f0f6f3773dea4437b7fd4850de25a20a",
    base_url="https://api.deepseek.com"
)


def ask_llm(question, context, use_rag=True):
    if use_rag:
        user_content = f"""
    用户问题：
    {question}

    可参考资料：
    {context}

    请优先结合参考资料回答。
    如果参考资料不够，也可以用你的通用知识补充。
    """
    else:
        user_content = f"""
    用户问题：
    {question}

    这个问题不需要参考知识库，请直接像正常中文AI助手一样回答。
    """

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {
                "role": "system",
                "content": """
    你是一个中文AI助手。

    规则：
    1. 用中文回答
    2. 每次只回复一条消息
    3. 不要描述场景
    4. 回复简短自然，像微信聊天一样
    5. 有需要可以用表情
    """
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    return response.choices[0].message.content