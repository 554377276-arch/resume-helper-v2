# LangChain RAG Agent Chatbot

基于 **FastAPI + DeepSeek + FAISS + LangChain** 构建的 RAG / Agent 智能问答系统。

本项目从基础 RAG 问答系统逐步升级为 Agent 应用，支持网页聊天、SQLite 历史记录、知识库检索、FAISS 向量搜索、DeepSeek 大模型调用、手写 Agent 工具路由，以及 LangChain Agent 工程化接入。

---


## 项目简介

本项目是一个 AI 应用开发项目，目标是实现一个支持多轮对话、知识库检索和工具调用的智能问答系统。

系统支持用户在网页中进行对话，并由后端 Agent 根据问题类型自动选择合适工具：

```text
用户问题
↓
多轮上下文处理
↓
Agent 判断是否需要工具
↓
RAG / DB / LLM 工具调用
↓
LLM 整理最终回答
↓
网页展示结果
```

项目重点不只是调用大模型，而是完整实现了一个 AI 应用中的核心链路：

* FastAPI 后端接口
* 前端聊天页面
* SQLite 聊天记录
* RAG 知识库检索
* FAISS 向量库
* DeepSeek LLM 调用
* 手写 Agent 流程
* LangChain Agent 工程化升级
* 多轮上下文问题改写

---

## 技术栈

| 模块        | 技术                      |
| --------- | ----------------------- |
| 后端框架      | FastAPI                 |
| 前端页面      | HTML / CSS / JavaScript |
| 模板引擎      | Jinja2                  |
| 大模型       | DeepSeek                |
| Agent 框架  | LangChain               |
| 向量检索      | FAISS                   |
| Embedding | SentenceTransformer     |
| 数据库       | SQLite                  |
| 版本管理      | Git / GitHub            |

---
## 项目截图

<img width="1122" height="859" alt="image" src="https://github.com/user-attachments/assets/77551c1b-be3d-4671-890a-b30aae895ff6" />

## 核心功能

### 1. 网页聊天系统

项目提供类 ChatGPT 的网页聊天界面，用户可以直接在网页中输入问题，并查看 AI 返回结果。

前端通过 `fetch` 请求 FastAPI 后端接口：

```text
前端输入
↓
POST /langchain-agent
↓
LangChain Agent
↓
返回回答
```

---

### 2. SQLite 聊天记录

项目使用 SQLite 保存历史对话，支持：

* 新建对话
* 查看历史对话
* 加载历史消息
* 删除历史对话
* 多轮上下文传递

---

### 3. RAG 知识库检索

项目支持上传 TXT 文件作为知识库资料。

RAG 流程：

```text
知识库文本
↓
文本切分 chunk
↓
Embedding 向量化
↓
FAISS 相似度检索
↓
返回相关上下文
↓
LLM 生成回答
```

RAG 工具适合处理知识库已有内容，例如：

* 地方美食推荐
* 旅游资料问答
* 文档内容检索
* 知识库相关问题

---

### 4. FAISS 向量检索

项目使用 FAISS 作为本地向量检索工具，相比简单关键词匹配，FAISS 可以根据语义相似度检索更相关的文本片段。

---

### 5. DeepSeek LLM 调用

项目通过 DeepSeek API 调用大模型生成回答。

API Key 使用环境变量读取，避免密钥直接写入代码。

环境变量名称：

```text
DEEPSEEK_API_KEY
```

Windows PowerShell 示例：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

---

## Agent 设计

本项目保留了两个 Agent 版本，方便展示从手写 Agent 到 LangChain Agent 的工程化升级过程。

---

### 1. 手写 Agent

在接入 LangChain 前，项目先实现了一个手写 Agent，核心模块包括：

* `TOOLS`：工具注册表
* `route_tool`：工具路由
* `execute_tool`：工具执行器
* `rewrite_query_with_history`：上下文问题改写
* `summarize_result`：工具结果整理

手写 Agent 流程：

```text
用户问题
↓
rewrite_query_with_history
↓
route_tool
↓
execute_tool
↓
rag_tool / db_tool / llm_tool
↓
summarize_result
↓
最终回答
```

这个阶段主要用于理解 Agent 的底层工作方式：工具注册、工具选择、工具执行和结果整理。

---

### 2. LangChain Agent

在手写 Agent 跑通后，项目进一步接入 LangChain：

* 将 `rag_tool` 包装成 LangChain Tool
* 将 `db_tool` 包装成 LangChain Tool
* 将 `llm_tool` 包装成 LangChain Tool
* 使用 LangChain Agent 自动选择工具
* 通过 FastAPI `/langchain-agent` 接口接入网页

LangChain Agent 流程：

```text
用户问题
↓
history 多轮上下文
↓
rewrite_query_with_history 问题改写
↓
LangChain Agent
↓
自动选择 Tool
↓
工具返回结果
↓
LLM 整理最终回答
```

项目没有简单丢弃手写逻辑，而是保留了 `rewrite_query_with_history`，让它负责稳定的上下文改写，再交给 LangChain Agent 进行工具选择和执行。

---

## 工具说明

项目中 Agent 可以使用三个工具：

| 工具         | 作用           |
| ---------- | ------------ |
| `rag_tool` | 查询 RAG 知识库内容 |
| `db_tool`  | 查询结构化演示数据    |
| `llm_tool` | 处理普通大模型问答    |

示例：

```text
用户：成都有什么好吃的？
↓
Agent 选择 rag_tool
↓
返回知识库中的成都美食内容
```

```text
用户：张三的爱好是什么？
↓
Agent 选择 db_tool
↓
返回张三的结构化信息
```

```text
用户：用一句话解释什么是 FastAPI
↓
Agent 不调用工具
↓
由 LLM 直接回答
```

---

## 多轮上下文处理

项目支持多轮上下文。

例如：

```text
用户：张三的爱好是什么？
AI：张三的爱好是睡觉。
用户：他几岁？
```

系统会结合历史记录，将“他”理解为“张三”，再交给 Agent 选择合适工具查询。

处理流程：

```text
当前问题 + 历史消息
↓
rewrite_query_with_history
↓
补全指代关系
↓
LangChain Agent
↓
工具调用 / 直接回答
```

---

## 项目结构

```text
langchain-rag-agent-chatbot
│
├─ agent
│  ├─ agent.py              # 手写 Agent：路由、执行、上下文改写
│  ├─ tools.py              # rag_tool / db_tool / llm_tool
│  ├─ langchain_tools.py    # LangChain Tool 包装层
│  └─ langchain_agent.py    # LangChain Agent 正式入口
│
├─ documents
│  └─ knowledge.txt         # RAG 知识库文本
│
├─ rag
│  └─ retriever.py          # RAG 检索与 FAISS 向量检索
│
├─ static
│  ├─ app.js                # 前端交互逻辑
│  └─ style.css             # 页面样式
│
├─ templates
│  └─ index.html            # 网页模板
│
├─ db.py                    # SQLite 聊天记录操作
├─ llm.py                   # DeepSeek LLM 调用
├─ main.py                  # FastAPI 主入口
├─ requirements.txt         # 项目依赖
└─ README.md
```

---

## 运行方式

### 1. 克隆项目

```bash
git clone <你的仓库地址>
cd langchain-rag-agent-chatbot
```

---

### 2. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. 安装依赖

```powershell
pip install -r requirements.txt
```

---

### 4. 配置 DeepSeek API Key

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

注意：不要将真实 API Key 写入代码或上传到 GitHub。

---

### 5. 启动项目

```powershell
uvicorn main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000/
```

---

## 主要接口

### 首页

```text
GET /
```

返回网页聊天页面。

---

### LangChain Agent 问答接口

```text
POST /langchain-agent
```

请求示例：

```json
{
  "query": "成都有什么好吃的？",
  "history": []
}
```

返回示例：

```json
{
  "query": "成都有什么好吃的？",
  "tool": "LANGCHAIN_AGENT",
  "result": "成都可以吃火锅、串串、兔头、冒菜等。"
}
```

---

### 手写 Agent 问答接口

```text
POST /agent
```

用于保留手写 Agent 版本，方便对比 LangChain Agent。

---

### 上传知识库

```text
POST /upload
```

用于上传 TXT 知识库文件，并刷新 RAG 检索内容。

---

### 聊天记录接口

```text
GET /chats
POST /chats
GET /chats/{chat_id}/messages
POST /chats/{chat_id}/messages
DELETE /chats/{chat_id}
```

用于管理 SQLite 聊天历史。

---

## 版本记录

本项目使用 Git Tag 记录阶段版本：

| Tag              | 说明                    |
| ---------------- | --------------------- |
| `v1.0-rag`       | RAG + FAISS 知识库检索版本   |
| `v2.0-agent`     | 手写 Agent 工具路由版本       |
| `v3.0-langchain` | LangChain Agent 工程化版本 |

---

## 项目亮点

### 1. 先手写 Agent，再接入 LangChain

项目不是一开始就套用框架，而是先手写 Agent 核心流程，包括工具注册、工具路由、工具执行和上下文改写。

之后再将工具迁移为 LangChain Tool，并使用 LangChain Agent 接管工具选择和执行流程。

---

### 2. 保留手写 Agent 与 LangChain Agent 双版本

项目中同时保留：

```text
/agent              → 手写 Agent
/langchain-agent    → LangChain Agent
```

这样可以清楚展示从底层实现到框架化迁移的过程。

---

### 3. RAG 与 Agent 结合

项目不是单纯 RAG 问答，而是让 Agent 根据问题类型判断是否需要调用工具：

```text
知识库问题 → rag_tool
结构化数据问题 → db_tool
普通问题 → LLM 直接回答
```

---

### 4. 支持多轮上下文

项目支持历史消息传入，并复用 `rewrite_query_with_history` 对上下文指代问题进行补全。

例如：

```text
用户：张三的爱好是什么？
用户：他几岁？
```

系统会将“他”结合历史理解为“张三”。

---

### 5. Git Tag 阶段版本管理

项目使用 Git Tag 保存不同开发阶段，便于查看项目演进过程：

```text
v1.0-rag
v2.0-agent
v3.0-langchain
```

---

## 后续优化方向

* 支持 Markdown / PDF 等更多知识库文件格式
* 将 DB 工具从演示数据升级为 JSON / SQLite / MySQL 数据源
* 增加 LangSmith 调试与链路追踪
* 使用 LangGraph 编排更复杂的 Agent 工作流
* 优化前端聊天 UI
* 增加更完整的异常处理和日志系统

---

## 项目定位

这是一个 AI 应用开发学习项目，重点展示以下能力：

* FastAPI Web 应用开发
* RAG 检索增强生成
* FAISS 向量检索
* DeepSeek LLM 接入
* Agent 工具调用设计
* LangChain 工程化接入
* 多轮上下文处理
* Git / GitHub 阶段版本管理

