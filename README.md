# 这是一个从 RAG 问答系统升级而来的基础 Agent 项目

手写版基础 Agent 原型

## 功能

- RAG检索增强生成
- 多轮对话
- 历史聊天记录
- SQLite存储
- TXT知识库上传
- FAISS向量检索
## 项目亮点

- 使用 SentenceTransformer 生成文本向量
- 使用 FAISS 构建向量索引
- 使用 DeepSeek 实现大模型问答
- 基于 FastAPI 搭建 Web 服务
- 使用 SQLite 保存聊天记录
- 支持上传知识库并实时刷新向量索引
## 技术栈

Python
FastAPI
DeepSeek
SentenceTransformer
FAISS
SQLite
HTML
CSS
JavaScript

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
