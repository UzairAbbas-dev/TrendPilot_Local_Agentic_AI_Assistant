#  TrendPilot: Testing & Error Analysis

This document contains the formal test records and system debugging logs for the TrendPilot Agentic AI Assistant, as required by the PITB AIRI Task 2 assignment.

## Part 1: Agent Test Cases (10 Iterations)
To ensure the agent handles diverse technical and non-technical prompts effectively, it was tested across different topics, platforms, and tones. All test cases successfully triggered the multi-tool workflow and saved a final `.md` artifact.

| Test No. | Input Topic | Target Platform | Requested Tone | Expected Output / Tools Used | Result & Saved File |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | YOLOv8 helmet safety detection project | LinkedIn | Professional + Exciting | All Tools. Expected a structured post, script, and tags. | **Useful (Passed)** - `YOLOv8_helmet_safety_20260906.md` |
| **2** | Using FinalRecon for domain footprinting in Kali Linux | X / Twitter | Technical & Educational | Ideas, Caption, Tags, Saver. Expected a short thread intro. | **Useful (Passed)** - `Using_FinalRecon_for_dom_20260906.md` |
| **3** | Debugging PyTorch `CUDA out of memory` errors | Instagram Reels | Humorous / Meme Style | Script, Tags, QA, Saver. Expected a funny visual breakdown. | **Useful (Passed)** - `Debugging_PyTorch_CUDA_20260906.md` |
| **4** | Comparing RT-DETR vs YOLO object detection | LinkedIn | Professional + Exciting | All Tools. Expected deep technical contrast. | **Useful (Passed)** - `Comparing_RT-DETR_vs_YOL_20260907.md` |
| **5** | 6-month AI Internship Lessons at PITB | LinkedIn | Storytelling / Vulnerable | Ideas, Caption, QA, Saver. Expected a personal narrative. | **Useful (Passed)** - `6-month_AI_Internship_Le_20260907.md` |
| **6** | Deploying MLflow tracking server using Docker | YouTube Shorts | Technical & Educational | Script, Tags, Saver. Expected fast-paced technical visuals. | **Useful (Passed)** - `Deploying_MLflow_trackin_20260907.md` |
| **7** | Model worked in Dev, Failed in Production | TikTok | Humorous / Meme Style | Script, Tags, QA, Saver. Expected a relatable 30s video. | **Useful (Passed)** - `Model_worked_in_Dev_Fail_20260907.md` |
| **8** | Configuring UFW firewall rules on Ubuntu | X / Twitter | Technical & Educational | Ideas, Caption, Tags, Saver. Expected concise bash commands. | **Useful (Passed)** - `Configuring_UFW_firewall_20260907.md` |
| **9** | Data Labeling struggles (annotating 10k images) | Instagram Reels | Storytelling / Vulnerable | Script, Caption, Saver. Expected an emotive, relatable angle. | **Useful (Passed)** - `Data_Labeling_struggles__20260907.md` |
| **10**| AI proctoring system using OpenCV | LinkedIn | Professional + Exciting | All Tools. Expected a strong project showcase with a clear CTA. | **Useful (Passed)** - `AI_proctoring_system_usi_20260907.md` |

---

## Part 2: Error Analysis & System Correction (5 Weak Responses)

Local models like Gemma 3:4B and Llama 3.2:3B are highly capable but can struggle with strict formatting or process timeouts. Below is an analysis of 5 weak or failed responses during initial development, and the engineering fixes applied to solve them.

| Test Case | Problem Found | Possible Reason | Fix Applied |
| :--- | :--- | :--- | :--- |
| **YOLOv8 Project (Initial Run)** | File saving tool crashed with `FileNotFoundError`. | The user input string contained special characters (e.g., `:`) which are invalid for file naming in OS filesystems. | Added a Python regex sanitizer (`re.sub(r'[^a-zA-Z0-9_-]', '_', topic)`) to clean file names before saving. |
| **Comparing RT-DETR vs YOLO** | The application threw a `Read timed out` error and generated no output. | The local 4B model required >60 seconds to process long scripts. Python's default socket timeout killed the request. | Increased the `requests.post()` timeout limit from 60 seconds to 300 seconds in `app/tools.py`. |
| **Cybersecurity UFW Config** | The X/Twitter post generated was over 600 words long. | Small local LLMs default to writing long, blog-style paragraphs unless heavily constrained. | Improved the `CAPTION_WRITER_PROMPT` to enforce strict formatting and character awareness when the platform is "X / Twitter". |
| **Debugging PyTorch (Meme)** | The Reel Script was entirely text, reading like an essay instead of a video plan. | The prompt asked for a "video script" but didn't specify a temporal structure, confusing the model. | Added explicit pacing brackets to the prompt (e.g., `[0:00-0:05] Hook (Visual + Audio)`) to force short, scene-by-scene generation. |
| **MLflow Deployment** | The Hashtag tool included conversational filler: *"Sure, here are your hashtags: #MLflow..."* | Non-deterministic "chatty" behavior common in instruct-tuned local models. | Added a deterministic Python regex filter (`re.findall(r"#[A-Za-z0-9_]+")`) to the tool to mathematically extract only the tags. |

---

### System Improvements Proposed & Implemented:
1. **Added validation checks (Regex):** Replaced prompt-based begging with hardcoded regex extraction for hashtags and file names to guarantee system stability.
2. **Better Prompts (Structured Output):** Enforced strict layout rules in the system prompts (using Markdown headers and timestamp brackets) to control the LLM's output shape.
3. **Optimized Local Engine Configuration:** Modified HTTP request parameters (timeouts, temperature scaling) to better support heavy inference tasks running on a laptop CPU/iGPU.