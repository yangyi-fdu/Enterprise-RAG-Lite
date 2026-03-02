from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.memory import get_history, add_message
from app.llm_client import chat_with_llm
from app.rag import find_relevant_chunks
from app.config import Config # 🌟 引入配置

app = FastAPI()

# ... (CORS 中间件代码不变) ...

# 🌟 在这里加了一个可选参数 top_k
@app.get("/ask")
def ask_ai(question: str, session_id: str = "default_user", top_k: int = None):
    
    actual_top_k = top_k if top_k is not None else Config.DEFAULT_TOP_K
    context = find_relevant_chunks(question, top_k=actual_top_k)
    
    # 🌟 重点 1：记忆里只存用户最原始、最纯净的问题！绝不把小抄存进历史！
    add_message(session_id, "user", question)
    
    # 获取纯净的历史记录
    current_history = get_history(session_id)
    
    # 🌟 重点 2：克隆一份历史记录用来发给 LLM，不要弄脏原本的记忆
    messages_for_llm = current_history.copy()
    
    # 🌟 重点 3：只在【发送给大模型的最后一句话】上，做“狸猫换太子”的临时包装
    if context:
        enhanced_prompt = f"""
请严格根据以下【已知资料】回答用户的问题。如果资料中没有相关信息，请利用你的常识回答。

【已知资料】：
{context}

【当前问题】：
{question}
"""
        # 把要发送的最后一条消息，偷偷替换成带有小抄的版本
        messages_for_llm[-1] = {"role": "user", "content": enhanced_prompt}

    # 发送给大模型的是包装过的 messages_for_llm，但存进 memory 的还是纯净版！
    answer = chat_with_llm(messages_for_llm)
    
    add_message(session_id, "assistant", answer)
    
    return {"question": question, "answer": answer, "session_id": session_id}
