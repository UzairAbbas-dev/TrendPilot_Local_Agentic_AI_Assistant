from app.tools import TrendPilotTools, call_ollama, DEFAULT_MODEL
from app.prompts import PLANNER_PROMPT
from app.memory import AgentMemory

class TrendPilotAgent:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.tools = TrendPilotTools()
        self.memory = AgentMemory()
        self.logs = []

    def _log(self, message: str):
        print(message)
        self.logs.append(message)

    def run(self, topic: str, platform: str = "LinkedIn", tone: str = "Professional & Engaging") -> dict:
        self.logs = []
        self._log(f"[*] Starting TrendPilot Agent for topic: '{topic}'")
        
        # Step 1: Agent Planning
        self._log("\n[Phase 1: Planning]")
        plan_prompt = PLANNER_PROMPT.format(topic=topic, platform=platform, tone=tone)
        plan = call_ollama(plan_prompt, model=self.model)
        self._log(f"Generated Strategy Plan:\n{plan}\n")

        # Step 2: Tool Execution - Ideas
        self._log("[Tool Called]: Trend Idea Generator")
        angles = self.tools.tool_trend_idea_generator(topic, platform, tone, model=self.model)

        # Step 3: Tool Execution - Caption & Hook
        self._log("[Tool Called]: Caption Writer")
        caption_data = self.tools.tool_caption_writer(topic, platform, tone, angle=angles[:100], model=self.model)
        hook = caption_data["hook"]
        caption = caption_data["full_caption"]

        # Step 4: Tool Execution - Hashtags
        self._log("[Tool Called]: Hashtag Generator")
        hashtags = self.tools.tool_hashtag_generator(topic, platform, model=self.model)

        # Step 5: Tool Execution - Reel Script
        self._log("[Tool Called]: Reel Script Generator")
        script = self.tools.tool_reel_script_generator(topic, tone, model=self.model)

        # Step 6: Tool Execution - Content Reviewer
        self._log("[Tool Called]: Content Reviewer")
        review = self.tools.tool_content_reviewer(hook, caption, platform, model=self.model)

        # Step 7: Tool Execution - File Saver
        self._log("[Tool Called]: File Saver")
        result_payload = {
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "plan": plan,
            "hook": hook,
            "caption": caption,
            "hashtags": hashtags,
            "script": script,
            "review": review
        }
        saved_file = self.tools.tool_file_saver(result_payload)
        result_payload["saved_file"] = saved_file
        self._log(f"[✓] Artifact saved to: {saved_file}")

        # Step 8: Update Memory
        self.memory.save_run(topic, platform, tone, hook)
        self._log("[✓] Session context stored in memory.")

        return result_payload