# Resume Helper V2 - RAG & Agent 智能问答系统

这是一个基于 FastAPI、DeepSeek API、FAISS 和 SQLite 实现的 AI 应用项目。

项目最初是一个 RAG 知识库问答系统，后续在 RAG 基础上升级为基础 Agent 系统，支持根据用户问题自动选择不同工具进行回答。

当前 Agent 支持三类工具：

- RAG 工具：用于知识库语义检索
- DB 工具：用于结构化数据查询（当前为 fake_db 原型）
- LLM 工具：用于通用对话和兜底回答

同时项目实现了基础的上下文传递、问题改写和回答整理，让系统具备初步的多工具智能问答能力。

## 版本迭代

### v1.0-rag

基础 RAG 问答版本。

功能包括：

- FastAPI 后端接口
- Web 聊天页面
- TXT 知识库上传
- FAISS 向量检索
- DeepSeek LLM 回答
- SQLite 保存聊天记录

### v2.0-agent

在 RAG 基础上升级为基础 Agent 版本。

新增功能：

- Agent 工具路由
- RAG / DB / LLM 三类工具
- Rule Router 规则分流
- 上下文 history 传递
- 问题改写 Rewrite
- 工具结果总结 Summarizer
- 前端调用 `/agent` 接口
## 项目亮点

- 使用 SentenceTransformer 生成文本向量
- 使用 FAISS 构建向量索引
- 使用 DeepSeek 实现大模型问答
- 基于 FastAPI 搭建 Web 服务
- 使用 SQLite 保存聊天记录
- 支持上传知识库并实时刷新向量索引
## 当前功能

- 支持网页聊天
- 支持创建、切换、删除历史对话
- 支持上传 TXT 知识库并刷新 RAG
- 支持 FAISS 向量检索
- 支持 DeepSeek API 调用
- 支持 Agent 自动选择工具
- 支持 DB / RAG / LLM 工具分流
- 支持上下文改写，例如“他多少岁”“这里有什么好吃的”
- 支持工具结果整理成自然语言回答

## 项目截图

<img width="1122" height="859" alt="image" src="https://github.com/user-attachments/assets/77551c1b-be3d-4671-890a-b30aae895ff6" />
聊天界面支持：

- RAG知识库问答
- 多轮对话
- 历史聊天记录
- TXT知识库上传
## 启动项目

pip install -r requirements.txt

uvicorn main:app --reload

api key需要自己在llm填写
