import threading
from collections import defaultdict

from app.config import Config


class SessionStore:
    """Per-session conversation history with a sliding window.

    Only the user's original questions and the model's answers are stored.
    Retrieved context is added to the outgoing prompt but never written back,
    so old context cannot leak into later turns or grow the token count.
    """

    def __init__(self, max_length: int = Config.MAX_HISTORY_LENGTH):
        self.max_length = max_length
        self._sessions: dict[str, list[dict]] = defaultdict(list)
        self._lock = threading.Lock()

    def add(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            history = self._sessions[session_id]
            history.append({"role": role, "content": content})
            del history[:-self.max_length]

    def get(self, session_id: str) -> list[dict]:
        """Return a copy, so callers can modify it without touching the store."""
        with self._lock:
            return [dict(m) for m in self._sessions.get(session_id, [])]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
