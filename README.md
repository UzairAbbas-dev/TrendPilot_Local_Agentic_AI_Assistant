
#  TrendPilot: Local Agentic AI Assistant

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B?style=for-the-badge&logo=streamlit)

**An autonomous, privacy-first AI agent that plans, writes, critiques, and formats viral social media campaigns entirely on local hardware.**

> **Built by:** Uzair Abbas (BS Artificial Intelligence)  
> **Developed for:** AIRI Team PITB - AI Internship Task 2  
> **Mentor:** Omar Farooq (Associate AI/ML Engineer)

---

##  The Problem vs. The Solution

**The Problem:** Most AI wrappers are just reactive chatbots. You have to manually prompt them to write a hook, then prompt them again for hashtags, then prompt them again to fix their tone, and finally copy-paste everything manually into a text file.

**The Solution:** TrendPilot is a true **Agentic Workflow**. You give it a single topic (e.g., *"YOLOv8 helmet detection"*). It automatically breaks the goal down into a strategic plan, routes specific tasks to specialized internal tools, critiques its own output, and saves a beautifully formatted Markdown file to your local drive.

---

##  System Architecture & Agent Workflow

TrendPilot doesn't just chat; it executes an orchestrated pipeline using `gemma3:4b` (or `llama3.2:3b`) running locally via Ollama.

1. **Strategic Planning:** The agent receives the topic, platform, and tone, then generates a 4-step execution plan.
2. **Tool Dispatch:** The agent sequentially invokes specialized Python tools:
   *  **Idea Generator:** Brainstorms 3 distinct psychological angles.
   *  **Caption Writer:** Drafts a scroll-stopping hook and structured body copy.
   *  **Script Director:** Generates a timestamped 30-45s video storyboard with audio/visual cues.
   *  **Regex Hashtag Generator:** Uses deterministic Python regex to strip conversational filler and extract clean hashtags.
3. **Self-Correction (QA):** The **Content Reviewer** evaluates the generated draft against platform standards and provides actionable feedback.
4. **State & Persistence:** 
   * **JSON Memory:** Logs the session to `outputs/memory_store.json` so the UI can track past runs.
   * **File Saver:** Sanitizes OS-level characters and exports the final payload as a `.md` file in `outputs/saved_results/`.

---

##  Tech Stack
* **Language:** Python 3.12
* **Local Inference:** Ollama API (`requests` library)
* **Web UI:** Streamlit
* **State Management:** JSON & Local File I/O

---

##  Installation & Setup

Because this project runs 100% locally, you will need to install Ollama to serve the LLM.

### 1. Install Ollama (Linux/Ubuntu)
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
ollama pull gemma3:4b

```

*(Verify it's running by typing `ollama --version` in your terminal).*

### 2. Clone the Repository & Setup Python

```bash
git clone [https://github.com/YourUsername/TrendPilot_Local_Agentic_AI_Assistant.git](https://github.com/YourUsername/TrendPilot_Local_Agentic_AI_Assistant.git)
cd TrendPilot_Local_Agentic_AI_Assistant

# Create and activate a fresh virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Run the Agent

**To launch the interactive Web UI (Recommended):**

```bash
streamlit run app/main.py

```

**To run the terminal CLI fallback:**

```bash
python demo.py

```

---

##  Project Structure

```text
TrendPilot_Local_Agentic_AI_Assistant/
│
├── app/
│   ├── __init__.py
│   ├── prompts.py       # Strict system prompts for tool boundaries
│   ├── tools.py         # The 6 agentic tools + API timeout handling
│   ├── memory.py        # JSON-backed conversational history
│   ├── agent.py         # The core execution loop (Plan -> Execute -> Review -> Save)
│   └── main.py          # Streamlit UI
│
├── outputs/
│   ├── saved_results/   # Auto-generated Markdown files live here
│   └── memory_store.json
│
├── tests/
│   └── test_cases.md    # 10 formal test cases & error analysis logs
│
├── screenshots/         # UI and Terminal execution proofs
├── requirements.txt
├── demo.py              # CLI runner
└── README.md

```

---

##  Engineering Notes & Lessons Learned

Developing for local hardware required overcoming specific inference challenges:

* **API Timeouts:** Smaller 4B parameter models running on CPU/iGPU require time to compute long, structured outputs (like video scripts). Python's default `requests` library drops sockets after 60 seconds. I engineered a fix by extending the socket timeout to `300s` in the tool definitions.
* **Non-Deterministic LLM Output:** Local models love to output conversational filler (*"Sure, here are your hashtags!"*). Instead of fighting the model with prompt engineering, I built a deterministic Python regex filter (`re.findall`) into the Hashtag Tool to guarantee clean data extraction.

---

*Created as part of the PITB Artificial Intelligence Internship Program (AIRI).*

