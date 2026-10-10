"""API tests with a fake retriever and LLM, so no model download or API key is needed."""
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from app import main
from app.config import Config
from app.memory import SessionStore
from app.retriever import Hit


class FakeRetriever:
    chunks = ["Leave: You get 15 days of annual leave."]

    def retrieve(self, query, top_k=3, min_similarity=0.0):
        if "leave" in query.lower():
            return [Hit(0, self.chunks[0], 0.8)]
        return []


class FakeLLM:
    def __init__(self):
        self.calls = []

    def chat(self, messages):
        self.calls.append(messages)
        return "15 days."


@asynccontextmanager
async def fake_lifespan(app):
    yield


@pytest.fixture
def client(monkeypatch):
    llm = FakeLLM()
    main.state.update(retriever=FakeRetriever(), llm=llm, memory=SessionStore())
    # Skip the real lifespan, so the embedding model and LLM client are never created.
    monkeypatch.setattr(main.app.router, "lifespan_context", fake_lifespan)
    with TestClient(main.app) as c:
        c.llm = llm
        yield c
    main.state.clear()


def test_in_scope_question_uses_context(client):
    r = client.post("/chat", json={"question": "How much annual leave?", "session_id": "a"})
    body = r.json()
    assert r.status_code == 200
    assert body["fallback"] is False
    assert body["sources"][0]["chunk_id"] == 0
    assert "15 days of annual leave" in client.llm.calls[0][-1]["content"]


def test_out_of_scope_question_falls_back_without_calling_the_llm(client):
    body = client.post("/chat", json={"question": "Capital of France?"}).json()
    assert body["fallback"] is True
    assert body["answer"] == Config.FALLBACK_ANSWER
    assert client.llm.calls == []


def test_history_stores_the_plain_question_not_the_context(client):
    client.post("/chat", json={"question": "How much annual leave?", "session_id": "a"})
    client.post("/chat", json={"question": "And leave carry-over?", "session_id": "a"})
    second_call = client.llm.calls[1]
    earlier_turns = second_call[1:-1]
    assert earlier_turns[0] == {"role": "user", "content": "How much annual leave?"}
    assert all("Context:" not in m["content"] for m in earlier_turns)


def test_empty_question_is_rejected(client):
    assert client.post("/chat", json={"question": ""}).status_code == 422
