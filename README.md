# Nexus — Smart Feedback Engine Planning Repo

**The working notes behind a hackathon project that adds evidence-linked, rubric-based AI feedback to an open-source LMS (SensAI): an implementation guide, a system-architecture flowchart and a set of coding-assistant skill files.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## Overview

SensAI is an AI-powered learning management system with a FastAPI backend and a Next.js frontend. The idea in this repo is a "Smart Feedback Engine" on top of it: take a learner's submission plus a rubric and return feedback that points at evidence (quotes, line references), says what to do next, and lets the learner re-submit and see how their scores change.

To be clear about what is in this repo: it does not contain the SensAI code or the engine implementation. It holds the plan and supporting material only:

- `CLAUDE.md`, the implementation guide I gave my coding assistant (architecture, constraints, key files, a feature-by-feature order).
- `generate_flowchart.py`, a script that draws the system-architecture flowchart, and its output `smart_feedback_engine_flowchart.png`.
- Four `*-SKILL.md` files (backend, FastAPI, frontend, Next.js) that are reference notes for the assistant.
- `.claude/settings.local.json`, a local list of allowed assistant shell commands.

The guide refers to `sensai-backend/` and `sensai-frontend/` folders, which are where the LMS code was meant to sit. Those are not part of this snapshot, so I cannot say here what was or was not implemented in them. Treat the feature list below as the plan, not as shipped behaviour.

## Key Features

These are the planned features from `CLAUDE.md`, in the order it sets out:

- **Working baseline (Feature 0)** — hardcoded prompt fallbacks in `api/routes/ai.py` for when Langfuse is not available, plus seed data (a published quiz, scorecards, knowledge-base context).
- **Evidence-linked feedback schema (Feature 1)** — adds `evidence`, `next_step`, `reasoning_gap` and `priority` fields to the output models.
- **Enhanced feedback display (Feature 2)** — evidence snippets, next-step guidance and priority-coded sections in `ScorecardView.tsx` and `LearnerScorecard.tsx`.
- **One-click re-evaluate (Feature 3)** — a button in `LearnerQuizView.tsx` that re-submits the edited answer while keeping history.
- **Feedback history timeline (Feature 4)** — an endpoint that reads scores out of `chat_history`, plus a timeline component.
- **Learner profile (Feature 5, stretch)** — a `learner_profiles` table whose contents are injected into prompts.

The flowchart also shows three priority tiers (critical, important, suggestion), Mermaid diagrams in the feedback, and a unified persistent chat. The guide does not describe those in detail.

## How It Works

The guide describes the existing SensAI flow that the engine builds on:

1. The frontend calls `POST /ai/chat` with `user_response`, `question_id` and `user_id`.
2. The backend loads the question and its scorecard from SQLite.
3. It fetches a prompt template with `langfuse.get_prompt()`. The guide marks this as broken without Langfuse access, which is why Feature 0 adds fallbacks.
4. The prompt is compiled with question and user details and the chat history is appended.
5. `stream_llm_with_openai()` in `api/llm.py` streams structured JSON, parsed incrementally with `jiter`.
6. The backend yields JSONL, one partial Pydantic model per line (all fields optional, built with `create_partial_model()`). The frontend reads them with `response.body.getReader()` and updates the UI as fields arrive.

Constraints written into the guide: a $5 OpenAI budget (use `gpt-4.1-mini` while developing, `gpt-4.1` for the demo), SQLite so no JSON queries, Judge0 CE self-hosted at `localhost:2358` for code execution (`docker-compose.judge0.yml`), Google OAuth through NextAuth.js, and a solo developer making small, surgical changes.

`generate_flowchart.py` uses matplotlib `FancyBboxPatch` boxes and annotated arrows to draw a 22 by 26 inch dark-theme diagram: problems on the left, the pipeline in the middle (learner submission, AI evaluation, objective vs subjective questions, evidence-linked feedback, feedback display, re-evaluate loop, score history and learner profile), solutions on the right.

## Tech Stack

- **Planned application stack (from `CLAUDE.md`):** FastAPI on Python 3.11+, Pydantic, SQLite, OpenAI API (`gpt-4.1`, `o3-mini`), Next.js 15 with React 19, NextAuth.js, Monaco Editor, Judge0 CE
- **Diagram script:** Python, matplotlib

## Getting Started

Only the flowchart script runs from this repo.

```bash
git clone https://github.com/Danushika06/Nexus.git
cd Nexus
pip install matplotlib
python generate_flowchart.py
```

The script writes the PNG to a hardcoded Windows path (`c:\Users\Danushika\Downloads\Nexus\...`). Change the path in the final `plt.savefig(...)` call before running it on another machine. I have not added a requirements file; matplotlib is the only third-party import.

## Project Structure

```
Nexus/
├── CLAUDE.md                            # implementation guide for the Smart Feedback Engine
├── generate_flowchart.py                # draws the architecture flowchart with matplotlib
├── smart_feedback_engine_flowchart.png  # the generated flowchart
├── backend-SKILL.md                     # assistant reference: backend engineering
├── fastapi-SKILL.md                     # assistant reference: FastAPI patterns
├── frontend-SKILL.md                    # assistant reference: frontend development
├── nextjs-SKILL.md                      # assistant reference: Next.js App Router
└── .claude/settings.local.json          # local allowed-commands list for the assistant
```

---

## Contact

<table>
  <tr><td><b>GitHub:</b> <a href="https://github.com/Danushika06">Danushika06</a></td><td><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/danushika-n-323b4628b/">danushika-n</a></td></tr>
  <tr><td colspan="2" align="center"><b>Email:</b> <a href="mailto:danushikanagarajan@gmail.com">danushikanagarajan@gmail.com</a></td></tr>
</table>

Built by **Danushika N**
