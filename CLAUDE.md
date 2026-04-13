# Smart Feedback Engine — Implementation Guide

## Project Overview
SensAI is an AI-powered LMS. We are building a **Smart Feedback Engine** that transforms
student submissions + rubrics into evidence-linked, actionable feedback with re-evaluation loops.

## Architecture
- **Backend**: FastAPI (Python 3.11+) at `sensai-backend/src/api/` — runs on `localhost:8001`
- **Frontend**: Next.js 15 + React 19 at `sensai-frontend/` — runs on `localhost:3000`
- **Database**: SQLite at `sensai-backend/src/db/db.sqlite`
- **LLM**: OpenAI API (gpt-4.1, o3-mini) via `api/llm.py` — $5 budget, minimize calls
- **Auth**: Google OAuth via NextAuth.js
- **Code Editor**: Monaco Editor in `CodeEditorView.tsx`
- **Code Execution**: Judge0 CE (self-hosted) at `localhost:2358` via `routes/code.py`

## Critical Constraints
- **No Langfuse access** — all prompts must be hardcoded as fallback in `api/routes/ai.py`
- **Judge0 CE** — self-hosted code execution engine at `localhost:2358` (see `docker-compose.judge0.yml`)
- **$5 OpenAI limit** — use gpt-4.1-mini for dev/testing, gpt-4.1 for demo only
- **SQLite** — no JSON queries, parse at application layer
- **Solo developer** — keep changes minimal and surgical

## Key Files (Backend)
- `sensai-backend/src/api/routes/ai.py` — AI chat/assignment endpoints (THE core file)
- `sensai-backend/src/api/llm.py` — OpenAI streaming with jiter partial JSON parsing
- `sensai-backend/src/api/models.py` — All Pydantic request/response models
- `sensai-backend/src/api/config.py` — Model names, table names, paths
- `sensai-backend/src/api/db/chat.py` — Chat history CRUD
- `sensai-backend/src/api/db/task.py` — Task/question/scorecard DB operations
- `sensai-backend/src/api/db/__init__.py` — Table schemas and init_db()
- `sensai-backend/src/api/routes/scorecard.py` — Scorecard CRUD
- `sensai-backend/src/api/routes/chat.py` — Chat history endpoints

## Key Files (Frontend)
- `sensai-frontend/src/components/LearnerQuizView.tsx` — Quiz submission + streaming
- `sensai-frontend/src/components/LearnerAssignmentView.tsx` — Assignment submission
- `sensai-frontend/src/components/ChatView.tsx` — Chat display with AI messages
- `sensai-frontend/src/components/ScorecardView.tsx` — Scorecard criterion display
- `sensai-frontend/src/components/LearnerScorecard.tsx` — Score bar rendering
- `sensai-frontend/src/components/CodeEditorView.tsx` — Monaco editor
- `sensai-frontend/src/types/quiz.ts` — TypeScript types for chat/scorecard

## How the AI Flow Works (Current)
1. Frontend calls `POST /ai/chat` with user_response, question_id, user_id
2. Backend fetches question + scorecard from DB
3. Backend calls `langfuse.get_prompt()` to get prompt template (BROKEN without Langfuse)
4. Prompt is compiled with question_details, user_details
5. Chat history is appended as messages
6. `stream_llm_with_openai()` streams structured JSON via jiter partial parsing
7. Frontend reads JSONL stream, renders ChatView + ScorecardView

## How Streaming Works
- Backend yields JSONL (one JSON object per line)
- Each chunk is a partial Pydantic model (all fields Optional via `create_partial_model()`)
- Frontend reads chunks via `response.body.getReader()`, parses each line as JSON
- UI updates progressively as fields become available

## Implementation Rules
1. **Feature-by-feature only** — plan, implement, test one feature completely before moving on
2. **Test manually after each feature** — verify on localhost:3000 + localhost:8001
3. **Minimize OpenAI calls** — use gpt-4.1-mini during development, switch for demo
4. **Don't break existing functionality** — all changes must be backward-compatible
5. **Keep changes surgical** — modify existing files, don't create unnecessary new files
6. **Explain each change** — describe what is being done and why before implementing

## Feature Implementation Order

### Feature 0: Make System Functional (BLOCKER)
**Problem**: `langfuse.get_prompt()` will fail without Langfuse access.
**Solution**: Add hardcoded prompt fallbacks that activate when Langfuse is unavailable.
**Also**: Seed database with published quiz questions + scorecards for testing.
**Files**: `ai.py` (prompt fallbacks), seed script
**Test**: Submit a text answer to a quiz question, verify AI feedback streams back.

### Feature 1: Evidence-Linked Feedback Schema
**Problem**: Current feedback is flat text (`correct`/`wrong` strings per criterion).
**Solution**: Add `evidence`, `next_step`, `reasoning_gap`, `priority` fields to output models.
**Files**: `ai.py` (Pydantic models + prompt instructions)
**Test**: Submit code/text, verify JSON response includes evidence with snippets and line refs.

### Feature 2: Enhanced Feedback Display
**Problem**: ScorecardView only shows progress bars + expand text.
**Solution**: Render evidence snippets, next-step guidance, priority-coded sections.
**Files**: `ScorecardView.tsx`, `LearnerScorecard.tsx`, `quiz.ts` (types)
**Test**: Submit answer, verify frontend shows evidence + next steps + color-coded priority.

### Feature 3: One-Click Re-Evaluate
**Problem**: No dedicated re-evaluate button; retry deletes previous messages.
**Solution**: Add "Re-evaluate" button that re-submits current content preserving history.
**Files**: `LearnerQuizView.tsx`
**Test**: Submit, get feedback, edit answer, click re-evaluate, verify new feedback appears.

### Feature 4: Feedback History Timeline
**Problem**: No way to see score progression across attempts.
**Solution**: Backend endpoint extracts scores from chat_history; frontend shows timeline.
**Files**: New endpoint in chat routes, new timeline component
**Test**: Make 2-3 submissions, verify timeline shows score changes per criterion.

### Feature 5: Learner Profile (Stretch)
**Problem**: AI doesn't know student's patterns across questions.
**Solution**: New learner_profiles table, populate from evaluation results, inject into prompts.
**Files**: New DB table, new DB operations, ai.py prompt injection
**Test**: Submit multiple answers, verify AI references student patterns in feedback.

## Database Seeding Required
- 1 published quiz task with 2-3 questions (objective + subjective with code)
- Scorecards linked to subjective questions
- Questions with knowledge base context
- All linked to existing course (id=4) and org (id=1)

## Testing Approach
- Backend: Hit endpoints via Swagger at localhost:8001/docs
- Frontend: Navigate to learner view, submit answers, verify UI
- Watch terminal logs for errors on both servers
