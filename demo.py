from app.agent import TrendPilotAgent

def main():
    print("="*60)
    print("      TrendPilot CLI Agent (Local Ollama Engine)")
    print("="*60)

    topic = input("Enter your topic: ").strip() or "YOLOv8 real-time object detection"
    platform = input("Choose platform [LinkedIn/Instagram/X]: ").strip() or "LinkedIn"
    tone = input("Choose tone [Professional/Humorous/Technical]: ").strip() or "Professional"

    agent = TrendPilotAgent()
    result = agent.run(topic=topic, platform=platform, tone=tone)

    print("\n" + "="*60)
    print(f"Agent Finished Execution! File: {result['saved_file']}")
    print("="*60)
    print("\n[HOOK]:\n", result["hook"])
    print("\n[HASHTAGS]:\n", " ".join(result["hashtags"]))

if __name__ == "__main__":
    main()