import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as pe

# Try to use Segoe UI Emoji for emoji support on Windows
plt.rcParams['font.family'] = ['Segoe UI', 'DejaVu Sans']

fig = plt.figure(figsize=(22, 26), facecolor='#0A0F1E')
ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
ax.set_xlim(0, 22)
ax.set_ylim(0, 26)
ax.set_facecolor('#0A0F1E')
ax.axis('off')

# ── helpers ──────────────────────────────────────────────────────────────────

def box(cx, cy, w, h, fc, ec=None, lw=0, pad=0.12, z=2, alpha=1.0):
    p = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=fc, linewidth=lw,
        edgecolor=ec or fc, zorder=z, alpha=alpha)
    ax.add_patch(p)

def dot(cx, cy, r, color, z=3):
    c = Circle((cx, cy), r, color=color, zorder=z)
    ax.add_patch(c)

def txt(x, y, s, size=10, color='#F8FAFC', ha='center', va='center', bold=False, z=4):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
            fontweight='bold' if bold else 'normal', zorder=z,
            multialignment='center')

def arr(x1, y1, x2, y2, color='#64748B', lw=2.2, scale=18):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                mutation_scale=scale, connectionstyle='arc3,rad=0'),
                zorder=5)

def darr(x1, y1, x2, y2, color='#475569', lw=1.6, scale=13):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                mutation_scale=scale, linestyle='dashed'), zorder=4)

def divider(y, color='#1E293B', lw=1.0):
    ax.axhline(y, xmin=0.02, xmax=0.98, color=color, lw=lw, zorder=1, linestyle=':')

def step_badge(cx, cy, number, color, bg):
    """Small numbered circle to label each step."""
    dot(cx, cy, 0.28, bg, z=6)
    txt(cx, cy, str(number), size=8, color=color, bold=True, z=7)

# ── layout constants ─────────────────────────────────────────────────────────
CX  = 11.0
BW  = 7.8
BH  = 1.45
SBW = 5.8
LX  = 2.5
RX  = 19.5
SW  = 3.8
SH  = 1.2

Y_T = 25.1
Y1  = 23.0
Y2  = 21.0
Y3  = 18.9
Y4  = 16.4
Y5  = 13.9
Y6  = 11.5
Y7  =  9.1
Y8  =  6.8
Y_F =  1.1

# ── subtle background dots grid ───────────────────────────────────────────────
for gx in [x * 0.5 for x in range(0, 45)]:
    for gy in [y * 0.5 for y in range(0, 53)]:
        dot(gx, gy, 0.025, '#1E293B', z=0)

# ── TITLE ────────────────────────────────────────────────────────────────────
box(CX, Y_T, 21.5, 1.6, '#1E1B4B', ec='#4F46E5', lw=2.5, pad=0.18)
txt(CX, Y_T + 0.38, 'SMART FEEDBACK ENGINE  —  SYSTEM ARCHITECTURE',
    size=15, bold=True, color='#A5B4FC')
txt(CX, Y_T - 0.32,
    'Transforming student submissions + rubrics into evidence-linked, scalable mentor feedback',
    size=9.5, color='#818CF8')

# Column headers
box(LX, 24.1, SW, 0.65, '#450A0A', ec='#DC2626', lw=2, pad=0.1)
txt(LX, 24.1, 'PROBLEMS TODAY', size=10, bold=True, color='#FCA5A5')

box(RX, 24.1, SW, 0.65, '#052E16', ec='#16A34A', lw=2, pad=0.1)
txt(RX, 24.1, 'OUR SOLUTION', size=10, bold=True, color='#86EFAC')

# ── STEP 1 : LEARNER SUBMISSION ──────────────────────────────────────────────
step_badge(CX - BW/2 - 0.55, Y1, '1', '#C7D2FE', '#4F46E5')
box(CX, Y1, BW, BH, '#312E81', ec='#6366F1', lw=2.5)
txt(CX, Y1 + 0.33, 'LEARNER SUBMISSION', size=12.5, bold=True, color='#C7D2FE')
txt(CX, Y1 - 0.3, 'Code Solutions   |   Text Responses   |   Multi-step Answers',
    size=9.5, color='#A5B4FC')

arr(CX, Y1 - BH / 2, CX, Y2 + BH / 2, color='#6366F1', lw=2.8)

# ── STEP 2 : AI EVALUATION ENGINE ────────────────────────────────────────────
step_badge(CX - BW/2 - 0.55, Y2, '2', '#DDD6FE', '#5B21B6')
box(CX, Y2, BW, BH, '#2E1065', ec='#8B5CF6', lw=2.5)
txt(CX, Y2 + 0.33, 'AI EVALUATION ENGINE', size=12.5, bold=True, color='#DDD6FE')
txt(CX, Y2 - 0.3, 'GPT-4.1   |   Rubric Criteria   |   Learner Context & History',
    size=9.5, color='#C4B5FD')

arr(CX - 1.2, Y2 - BH / 2, CX - 3.7, Y3 + BH / 2, color='#8B5CF6', lw=2.2)
arr(CX + 1.2, Y2 - BH / 2, CX + 3.7, Y3 + BH / 2, color='#8B5CF6', lw=2.2)

# ── STEP 3 : OBJECTIVE / SUBJECTIVE ──────────────────────────────────────────
OX = CX - 3.8
SX = CX + 3.8

step_badge(OX - SBW/2 - 0.4, Y3, '3a', '#BAE6FD', '#1D4ED8')
box(OX, Y3, SBW, BH, '#1E3A5F', ec='#3B82F6', lw=2)
txt(OX, Y3 + 0.33, 'OBJECTIVE QUESTIONS', size=11, bold=True, color='#BAE6FD')
txt(OX, Y3 - 0.3, 'Binary grading  |  Evidence quote\nLine-number reference', size=8.5, color='#93C5FD')

step_badge(SX + SBW/2 + 0.4, Y3, '3b', '#A5F3FC', '#0E7490')
box(SX, Y3, SBW, BH, '#0C2A3D', ec='#06B6D4', lw=2)
txt(SX, Y3 + 0.33, 'SUBJECTIVE QUESTIONS', size=11, bold=True, color='#A5F3FC')
txt(SX, Y3 - 0.3, 'Criterion scoring  |  Priority tiers\nScorecard generation', size=8.5, color='#67E8F9')

arr(OX + SBW / 2, Y3 - BH / 2, CX - 1.8, Y4 + 1.2, color='#3B82F6', lw=2)
arr(SX - SBW / 2, Y3 - BH / 2, CX + 1.8, Y4 + 1.2, color='#06B6D4', lw=2)

# ── STEP 4 : EVIDENCE-LINKED FEEDBACK ────────────────────────────────────────
step_badge(CX - (BW+2.5)/2 - 0.55, Y4, '4', '#A7F3D0', '#047857')
box(CX, Y4, BW + 2.5, 2.3, '#022C22', ec='#10B981', lw=2.5)
txt(CX, Y4 + 0.78, 'EVIDENCE-LINKED FEEDBACK', size=12.5, bold=True, color='#A7F3D0')

# Priority pills
for i, (lbl, bg, fg, ec_) in enumerate([
    ('CRITICAL',   '#7F1D1D', '#FCA5A5', '#EF4444'),
    ('IMPORTANT',  '#78350F', '#FDE68A', '#F59E0B'),
    ('SUGGESTION', '#1E3A5F', '#BAE6FD', '#3B82F6'),
]):
    px = CX - 2.4 + i * 2.4
    box(px, Y4 + 0.12, 2.15, 0.5, bg, ec=ec_, lw=2, pad=0.08)
    txt(px, Y4 + 0.12, lbl, size=8.5, color=fg, bold=True)

txt(CX, Y4 - 0.58,
    'Exact code snippets  |  Line-number references  |  Reasoning gaps  |  Next-step guidance',
    size=8.5, color='#6EE7B7')

arr(CX, Y4 - 1.15, CX, Y5 + 1.15, color='#10B981', lw=2.8)

# ── STEP 5 : FEEDBACK DISPLAY ─────────────────────────────────────────────────
step_badge(CX - (BW+2.5)/2 - 0.55, Y5, '5', '#FDE68A', '#B45309')
box(CX, Y5, BW + 2.5, 2.2, '#1C1108', ec='#D97706', lw=2.5)
txt(CX, Y5 + 0.72, 'FEEDBACK DISPLAY', size=12.5, bold=True, color='#FDE68A')

for i, (lbl, bg, fg) in enumerate([
    ('Scorecard', '#92400E', '#FDE68A'),
    ('Evidence',  '#064E3B', '#A7F3D0'),
    ('Next Step', '#1E3A5F', '#BAE6FD'),
    ('Diagram',   '#3B0764', '#DDD6FE'),
]):
    sx = CX - 2.85 + i * 2.0
    box(sx, Y5 + 0.1, 1.85, 0.5, bg, pad=0.08)
    txt(sx, Y5 + 0.1, lbl, size=8.5, bold=True, color=fg)

txt(CX, Y5 - 0.62,
    'Unified persistent chat   |   Mermaid visual diagrams   |   Priority-sorted criteria',
    size=8.5, color='#FCD34D')

arr(CX, Y5 - 1.1, CX, Y6 + BH / 2, color='#F59E0B', lw=2.8)

# ── STEP 6 : RE-EVALUATE ─────────────────────────────────────────────────────
step_badge(CX - BW/2 - 0.55, Y6, '6', '#FCA5A5', '#9B1C1C')
box(CX, Y6, BW, BH, '#450A0A', ec='#EF4444', lw=2.5)
txt(CX, Y6 + 0.33, 'ONE-CLICK RE-EVALUATE', size=12.5, bold=True, color='#FCA5A5')
txt(CX, Y6 - 0.3, 'Edit answer  |  Trigger new AI evaluation  |  History preserved',
    size=9.5, color='#F87171')

# Re-evaluate loop (right side)
LOOP_X = CX + BW / 2 + 1.3
ax.plot([CX + BW / 2, LOOP_X],   [Y6 + 0.3,  Y6 + 0.3],  color='#EF4444', lw=2.2, zorder=5)
ax.plot([LOOP_X,       LOOP_X],   [Y6 + 0.3,  Y5 - 0.35], color='#EF4444', lw=2.2, zorder=5)
ax.annotate('', xy=(CX + (BW+2.5)/2 + 0.06, Y5 - 0.35),
            xytext=(LOOP_X, Y5 - 0.35),
            arrowprops=dict(arrowstyle='->', color='#EF4444', lw=2.2, mutation_scale=16), zorder=5)
box(LOOP_X + 0.7, (Y5 + Y6) / 2, 1.35, 0.7, '#2D0A0A', ec='#EF4444', lw=1.5, pad=0.1)
txt(LOOP_X + 0.7, (Y5 + Y6) / 2, 'RE-EVAL\nLOOP', size=7.5, color='#FCA5A5', bold=True)

arr(CX - 1.1, Y6 - BH / 2, CX - 3.7, Y7 + BH / 2, color='#64748B', lw=2.2)
arr(CX + 1.1, Y6 - BH / 2, CX + 3.7, Y7 + BH / 2, color='#7C3AED', lw=2.2)

# ── STEP 7 : SCORE HISTORY + LEARNER PROFILE ──────────────────────────────────
SCX = CX - 3.8
PCX = CX + 3.8

step_badge(SCX - SBW/2 - 0.4, Y7, '7a', '#CBD5E1', '#334155')
box(SCX, Y7, SBW, BH, '#1A2535', ec='#64748B', lw=2)
txt(SCX, Y7 + 0.33, 'SCORE HISTORY', size=11, bold=True, color='#CBD5E1')
txt(SCX, Y7 - 0.3, 'Attempt progression  |  Criterion diffs\nBefore vs After comparison', size=8.5, color='#94A3B8')

step_badge(PCX + SBW/2 + 0.4, Y7, '7b', '#DDD6FE', '#5B21B6')
box(PCX, Y7, SBW, BH, '#1E0A3C', ec='#7C3AED', lw=2)
txt(PCX, Y7 + 0.33, 'LEARNER PROFILE', size=11, bold=True, color='#DDD6FE')
txt(PCX, Y7 - 0.3, 'AI-generated summary  |  Observation log\nPersonalized prompts  |  Admin view', size=8.5, color='#C4B5FD')

arr(SCX + SBW / 2, Y7 - BH / 2, CX - 1.5, Y8 + 0.95, color='#64748B', lw=2)
arr(PCX - SBW / 2, Y7 - BH / 2, CX + 1.5, Y8 + 0.95, color='#7C3AED', lw=2)

# ── OUTCOME ───────────────────────────────────────────────────────────────────
box(CX, Y8, BW + 3.5, 1.9, '#052E16', ec='#22C55E', lw=3, pad=0.18)
txt(CX, Y8 + 0.43, 'MENTOR-QUALITY FEEDBACK AT SCALE', size=13.5, bold=True, color='#86EFAC')
txt(CX, Y8 - 0.36,
    'Consistent   |   Evidence-Linked   |   Actionable   |   Personalized   |   Scalable',
    size=9.5, color='#4ADE80')

# Glow effect on outcome box
box(CX, Y8, BW + 3.7, 2.0, '#052E16', ec='#22C55E', lw=1, pad=0.18, alpha=0.3, z=1)

# ── FEATURE PILLS ROW ─────────────────────────────────────────────────────────
Y_PILLS = 5.3
features = [
    ('Evidence-Linked', '#1E3A5F', '#BAE6FD'),
    ('Priority Tiers',  '#78350F', '#FDE68A'),
    ('Visual Diagrams', '#3B0764', '#DDD6FE'),
    ('Re-eval Loop',    '#450A0A', '#FCA5A5'),
    ('Score History',   '#1A2535', '#CBD5E1'),
    ('Learner Profile', '#1E0A3C', '#C4B5FD'),
    ('Unified Chat',    '#022C22', '#A7F3D0'),
]
pill_w = 2.9
total_w = len(features) * pill_w
start_x = CX - total_w / 2 + pill_w / 2
txt(CX, Y_PILLS + 0.62, 'KEY FEATURES', size=9, bold=True, color='#64748B')
for i, (lbl, bg, fg) in enumerate(features):
    px = start_x + i * pill_w
    box(px, Y_PILLS, pill_w - 0.2, 0.58, bg, pad=0.1)
    txt(px, Y_PILLS, lbl, size=8.5, color=fg, bold=True)

# ── LEFT COLUMN : PROBLEMS ────────────────────────────────────────────────────
prob = [
    (Y2, 'Generic Feedback',    'Quality varies; lacks\nspecificity or depth'),
    (Y4, 'No Evidence Links',   "Learners don't know\nwhy they're wrong"),
    (Y6, 'Manual Re-eval',      'Fragmented loops;\nno history tracking'),
    (Y7, 'No Personalization',  'Same feedback for\nevery learner'),
]
for py, title, desc in prob:
    box(LX, py, SW, SH, '#2D0A0A', ec='#7F1D1D', lw=1.5, pad=0.12)
    txt(LX, py + 0.25, 'X  ' + title, size=9, bold=True, color='#FCA5A5')
    txt(LX, py - 0.24, desc, size=7.5, color='#F87171')
    darr(LX + SW / 2 + 0.08, py, CX - BW / 2 - 0.12, py, color='#7F1D1D', lw=1.8, scale=14)

# ── RIGHT COLUMN : SOLUTIONS ──────────────────────────────────────────────────
sol = [
    (Y2, 'Rubric Evaluation',  'Criterion-wise scoring\nwith GPT-4.1'),
    (Y4, 'Evidence-Linked',    'Exact quotes, line refs,\nnext-step guidance'),
    (Y6, 'One-Click Re-eval',  'Seamless loop;\nfull history preserved'),
    (Y7, 'Learner Profile',    'AI tracks patterns;\npersonalizes feedback'),
]
for sy, title, desc in sol:
    box(RX, sy, SW, SH, '#0A2D0A', ec='#14532D', lw=1.5, pad=0.12)
    txt(RX, sy + 0.25, 'V  ' + title, size=9, bold=True, color='#86EFAC')
    txt(RX, sy - 0.24, desc, size=7.5, color='#4ADE80')
    darr(CX + BW / 2 + 0.12, sy, RX - SW / 2 - 0.08, sy, color='#14532D', lw=1.8, scale=14)

# ── FOOTER ───────────────────────────────────────────────────────────────────
box(CX, Y_F, 21.5, 0.68, '#1E293B', pad=0.12)
txt(CX, Y_F,
    'SensAI  |  Smart Feedback Engine  |  FastAPI + Next.js + GPT-4.1  |  Hackathon 2025',
    size=9, color='#64748B')

plt.savefig(
    r'c:\Users\Danushika\Downloads\Nexus\smart_feedback_engine_flowchart.png',
    dpi=160, bbox_inches='tight',
    facecolor='#0A0F1E', edgecolor='none')
plt.close()
print("Saved successfully.")
