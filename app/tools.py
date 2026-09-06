import os
import json
import re
from datetime import datetime
import requests
from app.prompts import (
    IDEA_GENERATOR_PROMPT,
    CAPTION_WRITER_PROMPT,
    REEL_SCRIPT_PROMPT,
    HASHTAG_PROMPT,
    REVIEWER_PROMPT
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")  # or gemma2:2b / gemma3:4b

def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Invokes local Ollama server."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"[Tool Error] Failed to communicate with Ollama: {str(e)}"

class TrendPilotTools:
    @staticmethod
    def tool_trend_idea_generator(topic: str, platform: str, tone: str, model: str = DEFAULT_MODEL) -> str:
        prompt = IDEA_GENERATOR_PROMPT.format(topic=topic, platform=platform, tone=tone)
        return call_ollama(prompt, model=model)

    @staticmethod
    def tool_caption_writer(topic: str, platform: str, tone: str, angle: str, model: str = DEFAULT_MODEL) -> dict:
        prompt = CAPTION_WRITER_PROMPT.format(topic=topic, platform=platform, tone=tone, angle=angle)
        raw_output = call_ollama(prompt, model=model)
        
        # Simple extraction of hook vs body
        lines = [line.strip() for line in raw_output.split("\n") if line.strip()]
        hook = lines[0] if lines else "Unlock this AI secret today."
        return {"hook": hook, "full_caption": raw_output}

    @staticmethod
    def tool_reel_script_generator(topic: str, tone: str, model: str = DEFAULT_MODEL) -> str:
        prompt = REEL_SCRIPT_PROMPT.format(topic=topic, tone=tone)
        return call_ollama(prompt, model=model)

    @staticmethod
    def tool_hashtag_generator(topic: str, platform: str, model: str = DEFAULT_MODEL) -> list:
        prompt = HASHTAG_PROMPT.format(topic=topic, platform=platform)
        res = call_ollama(prompt, model=model)
        tags = re.findall(r"#[A-Za-z0-9_]+", res)
        return tags if tags else ["#AI", f"#{platform.replace(' ', '')}", "#TechInnovation"]

    @staticmethod
    def tool_content_reviewer(hook: str, caption: str, platform: str, model: str = DEFAULT_MODEL) -> str:
        prompt = REVIEWER_PROMPT.format(hook=hook, caption=caption, platform=platform)
        return call_ollama(prompt, model=model)

    @staticmethod
    def tool_file_saver(data: dict, base_dir: str = "outputs/saved_results") -> str:
        """Mandatory Tool: Saves markdown & JSON artifacts."""
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_title = re.sub(r'[^a-zA-Z0-9_-]', '_', data.get("topic", "content"))[:25]
        
        filename = f"{sanitized_title}_{timestamp}.md"
        filepath = os.path.join(base_dir, filename)
        
        md_content = f"""# TrendPilot Output: {data.get('topic')}

- **Platform:** {data.get('platform')}
- **Tone:** {data.get('tone')}
- **Generated At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 Viral Angle & Plan
{data.get('plan')}

---

## 🎣 Hook
> {data.get('hook')}

---

## 📝 Caption
{data.get('caption')}

---

## 🏷️ Hashtags
{' '.join(data.get('hashtags', []))}

---

## 🎬 30-45s Reel/Short Script
{data.get('script')}

---

## 🔍 Quality Review & Optimization
{data.get('review')}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        return filepath