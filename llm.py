import json
from openai import OpenAI
import os
client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def ask_llm(question, context, use_rag=True, history=""):

    messages = [
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
6. 如果用户追问“这个呢、那两个呢、再多一点呢”，要结合前面的聊天记录理解
"""
        }
    ]

    # 1. 把历史聊天加入 messages
    if history:
        try:
            history_list = json.loads(history)

            for msg in history_list[-6:]:
                role = "assistant" if msg["role"] == "ai" else "user"

                messages.append({
                    "role": role,
                    "content": msg["text"]
                })

        except Exception:
            pass

    # 2. 加当前问题 + RAG资料
    if use_rag:
        user_content = f"""
当前问题：
{question}

可参考资料：
{context}

如果资料相关，请结合资料回答。
如果资料不相关，请根据聊天记录和你的通用知识回答。
"""
    else:
        user_content = f"""
当前问题：
{question}

请根据聊天记录和你的通用知识回答。
"""

    messages.append({
        "role": "user",
        "content": user_content
    })

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages
    )

    return response.choices[0].message.content