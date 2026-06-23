import json
from llm import ask_llm
from agent.tools import rag_tool, db_tool, llm_tool

def summarize_result(query, tool_result):
    # 取出工具名称，例如 DB / RAG / LLM
    tool = tool_result.get("tool")

    # 取出工具返回的原始结果
    raw_result = tool_result.get("result")

    # 如果本来就是 LLM 回答，就不需要再整理一次
    if tool == "LLM":
        return tool_result

    prompt = f"""
你是一个回答整理器。

你的任务：
把工具返回的原始结果，整理成自然、简短、像聊天一样的中文回答。

用户问题：
{query}

工具类型：
{tool}

工具原始结果：
{raw_result}

要求：
1. 不要说“根据工具结果”
2. 不要输出JSON
3. 不要输出字典格式
4. 用中文自然回答
5. 回答简短一点
"""

    answer = ask_llm(
        question=prompt,
        context="",
        use_rag=False
    )

    return {
        "tool": tool,
        "result": answer
    }
def rewrite_query_with_history(query, history):
    print("📜 收到的history：", history)

    # 如果没有历史记录，就直接返回原问题
    if not history:
        return query

    # ================= 1. 先用规则处理“他 / 她 / 这个人” =================
    # 这些是我们假数据库里目前有的人名
    person_names = ["张三", "李四", "王五"]

    # 这些词表示用户在指代前面提到的人
    person_pronouns = ["他", "她", "这个人", "那个人"]

    # 判断当前问题里有没有“他、她、这个人、那个人”
    has_person_pronoun = False

    for pronoun in person_pronouns:
        if pronoun in query:
            has_person_pronoun = True

    # 如果当前问题里有人的指代词，就去历史记录里找最近出现的人名
    if has_person_pronoun:
        # reversed = 反向遍历，也就是从最近的聊天记录往前找
        for msg in reversed(history):
            text = msg.get("text", "")

            for name in person_names:
                if name in text:
                    new_query = query

                    # 把“他 / 她 / 这个人 / 那个人”替换成具体人名
                    for pronoun in person_pronouns:
                        new_query = new_query.replace(pronoun, name)

                    return new_query

    # ================= 2. 再用规则处理“这里 / 这边 / 本地” =================
    city_names = ["四川", "成都", "乐山", "绵阳", "宜宾"]

    place_pronouns = ["这里", "这边", "本地", "附近"]

    has_place_pronoun = False

    for pronoun in place_pronouns:
        if pronoun in query:
            has_place_pronoun = True

    if has_place_pronoun:
        for msg in reversed(history):
            text = msg.get("text", "")

            for city in city_names:
                if city in text:
                    new_query = query

                    for pronoun in place_pronouns:
                        new_query = new_query.replace(pronoun, city)

                    return new_query

    # ================= 3. 如果规则处理不了，再交给 LLM 改写 =================
    history_text = ""

    for msg in history[-6:]:
        role = msg.get("role")
        text = msg.get("text")

        history_text += f"{role}: {text}\n"

    prompt = f"""
你是一个问题改写器。

你的任务：
根据聊天历史，把用户当前问题改写成一个完整、明确的问题。

聊天历史：
{history_text}

当前问题：
{query}

要求：
1. 如果当前问题已经完整，就原样输出
2. 如果当前问题里有“他、她、它、这里、这个、那个、刚才”等指代词，要结合历史补全
3. 只输出改写后的问题
4. 不要解释
5. 不要输出JSON
"""

    rewritten_query = ask_llm(
        question=prompt,
        context="",
        use_rag=False
    )

    return rewritten_query.strip()
def agent(query, history=None):
    # 先结合聊天历史，把问题改写完整
    final_query = rewrite_query_with_history(query, history)

    print("📝 原始问题：", query)
    print("📝 改写后问题：", final_query)

    person_names = ["张三", "李四", "王五"]

    for name in person_names:
        if name in final_query:
            print("🧭 规则命中：人物信息 → DB")
            return summarize_result(final_query, db_tool(final_query))

    # 如果问题里出现这些关键词，直接走 RAG
    rag_keywords = ["四川", "美食", "好吃", "旅游", "成都", "乐山", "绵阳", "宜宾"]

    for word in rag_keywords:
        if word in final_query:
            print("🧭 规则命中：知识库问题 → RAG")
            return summarize_result(final_query, rag_tool(final_query))
    prompt = f"""
你是一个工具选择器。

你必须只输出JSON，不要任何解释：

{{
    "tool": "RAG" | "DB" | "LLM"
}}

规则：
- 如果是知识问题 → RAG
- 如果是用户信息查询 → DB
- 如果是闲聊/通用问题 → LLM

用户问题：
{final_query}
"""

    raw = ask_llm(prompt, context="").strip()

    print("\n🧠 原始LLM输出：", raw)

    # ===== 安全解析 =====
    try:
        choice = json.loads(raw)["tool"]
    except:
        choice = "LLM"

    print("🧠 解析后工具：", choice)

    # ===== 工具执行 =====
    if choice == "RAG":
        print("📚 使用RAG")
        return summarize_result(query, rag_tool(query))

    elif choice == "DB":
        print("🗄️ 使用DB")
        return summarize_result(query, db_tool(query))

    else:
        print("🤖 使用LLM")
        return llm_tool(final_query)