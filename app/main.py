import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import Config
from app.memory import SessionStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

SYSTEM_PROMPT = (
    "You are an internal assistant for company staff. Answer only from the "
    "context provided with the question. If the context does not contain the "
    "answer, say that you don't know. Keep answers short and quote exact numbers."
)

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Heavy objects are created once at startup; tests replace them in `state`.
    from app.llm_client import LLMClient
    from app.retriever import Retriever, load_embedding_model

    state["retriever"] = Retriever.from_file(Config.KNOWLEDGE_FILE, load_embedding_model())
    state["llm"] = LLMClient()
    state["memory"] = SessionStore()
    yield
    state.clear()


app = FastAPI(title="RAG Lite", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    session_id: str = "default"
    top_k: int = Field(default=Config.DEFAULT_TOP_K, ge=1, le=10)


class Source(BaseModel):
    chunk_id: int
    score: float
    text: str


class ChatResponse(BaseModel):
    answer: str
    fallback: bool
    sources: list[Source]
    session_id: str


def build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(f"[{i + 1}] {c}" for i, c in enumerate(context_chunks))
    return f"Context:\n{context}\n\nQuestion: {question}"


@app.get("/health")
def health():
    return {"status": "ok", "chunks": len(state["retriever"].chunks)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    retriever, llm, memory = state["retriever"], state["llm"], state["memory"]

    hits = retriever.retrieve(req.question, top_k=req.top_k)
    sources = [Source(chunk_id=h.chunk_id, score=round(h.score, 4), text=h.text) for h in hits]

    if not hits:
        # Out-of-scope question: answer with a fixed message instead of calling
        # the LLM, so it has no chance to make an answer up.
        answer = Config.FALLBACK_ANSWER
    else:
        # The stored history holds only the plain question; the context is
        # attached to the outgoing copy of the last message.
        history = memory.get(req.session_id)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history,
                    {"role": "user", "content": build_prompt(req.question, [h.text for h in hits])}]
        try:
            answer = llm.chat(messages)
        except Exception as exc:
            logging.exception("LLM call failed")
            raise HTTPException(status_code=502, detail="LLM request failed") from exc

    memory.add(req.session_id, "user", req.question)
    memory.add(req.session_id, "assistant", answer)
    return ChatResponse(answer=answer, fallback=not hits, sources=sources, session_id=req.session_id)


@app.delete("/sessions/{session_id}")
def clear_session(session_id: str):
    state["memory"].clear(session_id)
    return {"cleared": session_id}
