import json
from llm import ask_llm
from agent.tools import rag_tool, db_tool, llm_tool
# ================= 工具注册表 Tool Registry =================
# tool = 工具
# registry = 注册表 / 登记表
# 作用：把工具名称和真正的工具函数对应起来
TOOLS = {
    "RAG": rag_tool,
    "DB": db_tool,
    "LLM": llm_tool
}
# ================= 规则配置 Rule Config =================
# 这些人名命中后，优先走 DB 工具
PERSON_NAMES = ["张三", "李四", "王五"]

# 地点关键词
PLACE_KEYWORDS = ["四川", "成都", "乐山", "绵阳", "宜宾"]

# RAG 适合处理的意图关键词
# 现在你的知识库主要是美食/旅游类资料，所以不要只靠城市名触发 RAG
RAG_INTENT_KEYWORDS = ["美食", "好吃", "吃", "旅游", "玩", "推荐", "特色"]

# 当前还没有天气工具，所以天气类问题先走 LLM
WEATHER_KEYWORDS = ["天气", "气温", "下雨", "下雪", "冷不冷", "热不热"]

# 人称代词，用于上下文改写
PERSON_PRONOUNS = ["他", "她", "这个人", "那个人"]

# 地点代词，用于上下文改写
PLACE_PRONOUNS = ["这里", "这边", "本地", "附近"]

# 城市/地点词，用于上下文改写
CITY_NAMES = ["四川", "成都", "乐山", "绵阳", "宜宾"]
def execute_tool(tool_name, query):
    # 从工具注册表里取出工具函数
    # 如果找不到工具，默认使用 LLM 工具
    tool_func = TOOLS.get(tool_name, llm_tool)

    print("🧰 使用工具：", tool_name)

    # 执行工具
    tool_result = tool_func(query)

    # 如果是 LLM 工具，直接返回
    if tool_name == "LLM":
        return tool_result

    # 如果是 DB / RAG 工具，就整理成人话
    return summarize_result(query, tool_result)
def build_summarizer_prompt(query, tool, raw_result):
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

    return prompt
def summarize_result(query, tool_result):
    # 取出工具名称，例如 DB / RAG / LLM
    tool = tool_result.get("tool")

    # 取出工具返回的原始结果
    raw_result = tool_result.get("result")

    # 如果本来就是 LLM 回答，就不需要再整理一次
    if tool == "LLM":
        return tool_result

    prompt = build_summarizer_prompt(query, tool, raw_result)
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
    person_names = PERSON_NAMES
    # 这些词表示用户在指代前面提到的人
    person_pronouns = PERSON_PRONOUNS

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
    city_names = CITY_NAMES

    place_pronouns = PLACE_PRONOUNS

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
def build_router_prompt(final_query):
    prompt = f"""
你是一个工具选择器。

你只能从下面三个工具里选择一个：

1. RAG
用途：查询当前知识库中的文本资料。
适合：四川美食、成都美食、绵阳米粉、宜宾燃面、旅游推荐等知识库已有内容。
不适合：天气、实时新闻、股票、房价、当前时间等实时信息。

2. DB
用途：查询结构化人物信息。
适合：张三、李四、王五的年龄、爱好等信息。
不适合：普通聊天、城市知识、天气、美食推荐。

3. LLM
用途：通用回答和兜底回答。
适合：闲聊、解释概念、天气类泛回答、知识库没有覆盖的问题、无法判断的问题。

选择规则：
- 如果问题明确属于人物信息 → DB
- 如果问题明确属于当前知识库内容 → RAG
- 如果不确定，必须选择 LLM
- 不要因为问题里有城市名就选择 RAG
- 不要因为问题像“知识问题”就默认选择 RAG

你必须只输出JSON，不要任何解释：

{{
    "tool": "RAG" | "DB" | "LLM"
}}

用户问题：
{final_query}
"""

    return prompt

def route_tool(final_query):
    # ================= 1. 人物信息 → DB =================
    for name in PERSON_NAMES:
        if name in final_query:
            print("🧭 路由原因：命中人物名称")
            print("🧭 路由结果：DB")
            return "DB"

    # ================= 2. 天气问题 → LLM =================
    # 因为当前还没有 weather_tool 天气工具
    for word in WEATHER_KEYWORDS:
        if word in final_query:
            print("🧭 路由原因：命中天气类关键词")
            print("🧭 路由结果：LLM")
            return "LLM"

    # ================= 3. 地点 + RAG意图 → RAG =================
    has_place = False
    has_rag_intent = False

    for place in PLACE_KEYWORDS:
        if place in final_query:
            has_place = True

    for intent in RAG_INTENT_KEYWORDS:
        if intent in final_query:
            has_rag_intent = True

    if has_place and has_rag_intent:
        print("🧭 路由原因：命中地点 + RAG意图")
        print("🧭 路由结果：RAG")
        return "RAG"

    # ================= 4. 规则没命中 → 交给 LLM 判断 =================
    prompt = build_router_prompt(final_query)

    raw = ask_llm(prompt, context="").strip()

    print("\n🧠 原始LLM输出：", raw)

    try:
        choice = json.loads(raw)["tool"]
    except:
        choice = "LLM"

    print("🧠 解析后工具：", choice)
    print("🧭 路由原因：规则未命中，交给 LLM 选择工具")
    print("🧭 路由结果：", choice)

    return choice
def agent(query, history=None):
    print("\n================ Agent Start ================")

    # 先结合聊天历史，把问题改写完整
    final_query = rewrite_query_with_history(query, history)

    print("📝 原始问题：", query)
    print("📝 改写后问题：", final_query)

    # 路由器：判断应该使用哪个工具
    tool_name = route_tool(final_query)

    # 执行器：真正调用工具并返回结果
    return execute_tool(tool_name, final_query)