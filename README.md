# Enterprise-RAG-Lite: 企业级轻量化向量检索后端

## 🌟 项目介绍
本项目是一个从零手写的轻量级 RAG（检索增强生成）后端服务。主要解决了大模型在垂直领域应用中的“幻觉”、“上下文污染”等真实工程痛点。

## 💡 核心亮点
1. 向量语义检索：接入 FAISS 引擎与 Sentence-Transformers，实现毫秒级精准检索。
2. 滑动窗口切分：自主实现带 Overlap 的文档 Chunking 算法，解决长文本语义截断问题。
3. 动态阈值兜底：引入 L2 距离阈值校验，遇到知识盲区自动触发 Fallback 降级，阻断 AI 幻觉。
4. 纯净态记忆管理：实现多并发状态隔离与滑动窗口记忆，彻底根除上下文污染与 Token 爆炸。

## 🛠️ 技术栈
- 框架：FastAPI, Uvicorn
- 核心库：FAISS, Sentence-Transformers (MiniLM)
- 大模型：DeepSeek API
