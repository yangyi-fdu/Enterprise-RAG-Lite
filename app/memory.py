from app.config import Config

# 用一个字典来存储所有用户的记忆档案
sessions = {}

def add_message(session_id: str, role: str, content: str):
    """
    存入新消息，并执行“滑动窗口”截断逻辑
    """
    if session_id not in sessions:
        sessions[session_id] = []
        
    sessions[session_id].append({"role": role, "content": content})
    
    # 🌟 核心截断逻辑：如果历史记录超过了设定的最大限制
    if len(sessions[session_id]) > Config.MAX_HISTORY_LENGTH:
        # 切片魔法：只保留列表最后面的 MAX_HISTORY_LENGTH 条记录
        sessions[session_id] = sessions[session_id][-Config.MAX_HISTORY_LENGTH:]

def get_history(session_id: str) -> list:
    """
    取出某人的完整记忆档案
    """
    return sessions.get(session_id, [])
