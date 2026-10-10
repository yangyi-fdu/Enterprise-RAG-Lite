import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Knowledge base
    KNOWLEDGE_FILE = os.getenv("KNOWLEDGE_FILE", "data/handbook.md")
    EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

    # Chunking (measured in words). Overlap keeps facts that sit on a chunk
    # boundary retrievable from at least one chunk.
    CHUNK_SIZE = 60
    CHUNK_OVERLAP = 15

    # Retrieval
    DEFAULT_TOP_K = 3
    # Cosine similarity below this is treated as "not in the knowledge base".
    # Chosen with eval/eval_retrieval.py; see the README for the sweep.
    MIN_SIMILARITY = 0.30

    # Conversation memory: number of messages kept per session
    # (6 = the last 3 user/assistant exchanges).
    MAX_HISTORY_LENGTH = 6

    # LLM (any OpenAI-compatible endpoint)
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

    FALLBACK_ANSWER = (
        "I could not find this in the knowledge base, so I can't answer it reliably. "
        "Please contact the relevant team directly."
    )
