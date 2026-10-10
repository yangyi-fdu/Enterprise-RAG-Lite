from app.memory import SessionStore


def test_window_keeps_only_the_latest_messages():
    store = SessionStore(max_length=4)
    for i in range(10):
        store.add("s", "user", str(i))
    assert [m["content"] for m in store.get("s")] == ["6", "7", "8", "9"]


def test_sessions_are_isolated():
    store = SessionStore()
    store.add("alice", "user", "hello")
    assert store.get("bob") == []
    assert len(store.get("alice")) == 1


def test_get_returns_a_copy():
    store = SessionStore()
    store.add("s", "user", "original")
    history = store.get("s")
    history[0]["content"] = "modified"
    history.append({"role": "user", "content": "extra"})
    assert store.get("s") == [{"role": "user", "content": "original"}]
