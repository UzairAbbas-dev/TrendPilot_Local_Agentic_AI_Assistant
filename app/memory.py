import os
import json
from typing import List, Dict

MEMORY_FILE = "outputs/memory_store.json"

class AgentMemory:
    def __init__(self, storage_path: str = MEMORY_FILE):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_run(self, topic: str, platform: str, tone: str, summary: str):
        history = self.get_history()
        history.append({
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "summary": summary[:120] + "..."
        })
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(history[-10:], f, indent=2)  # Keep last 10 entries

    def get_history(self) -> List[Dict]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []