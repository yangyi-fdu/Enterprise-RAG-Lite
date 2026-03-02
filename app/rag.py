import os
import faiss
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from app.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    logger.info("⏳ 正在加载 SentenceTransformer 模型...")
    model = SentenceTransformer(Config.VECTOR_MODEL_NAME)
    logger.info("✅ 模型加载成功！")
except Exception as e:
    logger.error(f"❌ 模型加载失败: {e}")
    model = None

_knowledge_chunks = []
_faiss_index = None

# 🌟 新增函数：带有 Overlap 的滑动窗口切分算法
def split_text_with_overlap(text: str, chunk_size: int, overlap: int) -> list:
    chunks = []
    start = 0
    while start < len(text):
        # 截取从 start 开始，长度为 chunk_size 的文本
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        # 如果已经切到了文章末尾，就跳出循环
        if end == len(text):
            break
        # 🌟 关键点：下一个起点退后 overlap 个字，形成重叠区！
        start += (chunk_size - overlap)
    return chunks

def load_knowledge_base():
    global _knowledge_chunks, _faiss_index
    file_path = Config.KNOWLEDGE_FILE
    
    if not os.path.exists(file_path):
        logger.warning(f"⚠️ 找不到知识库文件: {file_path}")
        return

    try:
        # 🌟 现在的读取方式变了：我们把整个文件读成一整段巨大的长字符串
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read().replace("\n", " ").strip()
            
        if not full_text:
            logger.warning("⚠️ 知识库是空的！")
            return

        # 🌟 调用我们的高级切分算法
        _knowledge_chunks = split_text_with_overlap(
            full_text, 
            chunk_size=Config.CHUNK_SIZE, 
            overlap=Config.CHUNK_OVERLAP
        )

        logger.info(f"🧠 按 {Config.CHUNK_SIZE}字/块 (重叠{Config.CHUNK_OVERLAP}字) 切分完毕，共切出 {len(_knowledge_chunks)} 个 Chunk。")
        logger.info("正在构建 FAISS 索引...")
        
        embeddings = model.encode(_knowledge_chunks)
        dimension = embeddings.shape[1] 
        _faiss_index = faiss.IndexFlatL2(dimension)
        _faiss_index.add(np.array(embeddings))
        logger.info("✅ FAISS 向量库构建完成！")
        
    except Exception as e:
        logger.error(f"❌ 构建知识库时发生严重错误: {e}")

# ... (上面的代码保持不变，只改 find_relevant_chunks 函数) ...

def find_relevant_chunks(question: str, top_k: int = Config.DEFAULT_TOP_K) -> str:
    global _faiss_index, _knowledge_chunks
    
    if model is None:
        return ""
    if _faiss_index is None:
        load_knowledge_base()
    if _faiss_index is None or not _knowledge_chunks:
        return ""

    try:
        logger.info(f"🔍 收到检索请求: '{question}', 准备捞取前 {top_k} 条")
        question_embedding = model.encode([question])
        
        # D 是距离(分数)，I 是知识块的编号
        D, I = _faiss_index.search(np.array(question_embedding), top_k)
        
        best_chunks = []
        # 🌟 遍历检索结果的同时，严格检查“距离”是否及格
        for i in range(len(I[0])):
            idx = I[0][i]
            distance = D[0][i]  # 取出这条结果的距离得分
            
            if idx != -1 and idx < len(_knowledge_chunks):
                # 🌟 核心兜底逻辑：只有距离小于等于及格线，才算相关！
                if distance <= Config.MAX_DISTANCE:
                    best_chunks.append(_knowledge_chunks[idx])
                    logger.info(f"✅ 命中及格线: 距离 {distance:.2f} <= {Config.MAX_DISTANCE}")
                else:
                    logger.warning(f"❌ 过滤掉不相关资料: 距离 {distance:.2f} 太大 (兜底机制生效)")
                    
        # 🌟 如果过滤完之后，发现没有一个及格的资料
        if not best_chunks:
            logger.info("⚠️ 所有检索结果均不及格，触发 Fallback，退化为无小抄模式。")
            return ""
                
        logger.info(f"🎯 最终检索到最匹配的资料:\n" + "\n---\n".join(best_chunks))
        
        return "\n".join(best_chunks)
        
    except Exception as e:
        logger.error(f"❌ 检索过程中发生异常: {e}")
        return ""
