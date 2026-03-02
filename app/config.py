class Config:
    DEFAULT_TOP_K = 2
    KNOWLEDGE_FILE = "data/knowledge.txt"
    VECTOR_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    
    CHUNK_SIZE = 150
    CHUNK_OVERLAP = 30
    MAX_DISTANCE = 25.0 
    
    # 🌟 新增：对话历史最大保留条数 (控制 Token 消耗)
    # 设定为 6，意味着保留最近的 3 轮对话 (3个用户提问 + 3个AI回答)
    MAX_HISTORY_LENGTH = 6
