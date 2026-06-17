import os
from openai import OpenAI

# =========================
# 1. 创建客户端
# =========================
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# =========================
# 2. 调用LLM
# =========================
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": "你好，你是谁？"
        }
    ]
)

# =========================
# 3. 输出结果
# =========================
print(response.choices[0].message.content)