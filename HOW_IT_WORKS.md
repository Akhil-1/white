# How the code works (for the group, so you can explain it in class)

`app.py` is about 850 lines, in 12 numbered sections. Read it top to bottom once.

## The big idea
Streamlit **reruns the whole file from top to bottom every time the user clicks or types**.
So the file always: (1) styles the page, (2) reads the current inputs, (3) recalculates everything,
(4) draws only the current step.

## Section by section

| # | Section | What to say in class |
|---|---|---|
| 1 | Look and feel | `.streamlit/config.toml` sets the light theme (off-white page, deep-navy accent) so every native widget matches. One block of CSS in `app.py` then styles cards (white, hairline, soft shadow), the top bar, pills, option cards, the gold-ruled AI card and restyles Streamlit widgets (buttons, inputs, tabs, segmented controls). A `@media (max-width:760px)` block makes the phone layout: single column, 2×2 KPI tiles, step dots instead of labels, a sticky Back/Next bar. Small SVG icons and the ring/gauge are drawn in code (`icon()`, `ring()`, `gauge()`, `bar3()`). |
| 2 | Helpers | `inr()` formats ₹ in Indian style; `months_to_goal()` simulates saving month by month with growth until the target is reached; `path()` gives the month-by-month balance for the charts. |
| 3 | Session state | `st.session_state` holds the inputs while the user moves between steps. Sample numbers are pre-filled for the demo. Nothing is saved to disk. `go()` and `nav_changed()` keep the step buttons and the step tabs in sync. |
| 4 | The AI capability | `explain()` sends a **task** plus the **already-calculated facts** to Gemini with a fixed system prompt (use only given numbers, no fund names, no "best option", ≤80 words). If there is no key or the call fails, it shows a rule-based sentence instead, so the app never breaks. "What's sent to the AI" shows the exact JSON. |
| 5 | Calculations | Fixed rules: free money = salary − commitments − usual spend; buffer = savings ÷ monthly living costs; needed per month = (goal − saved) ÷ months left; risk comfort = score from 3 answers; each mix's expected return = weighted average of editable assumptions; likely range uses equity at 4% and 15%. |
| 6 | Charts | Altair, light theme. `goal_chart()` = savings lines with a dashed goal line, target-date line and hover tooltip (step 2). `range_chart()` = when each mix could reach the goal: dot = expected (with its date written next to it), bar = likely range, dashed line = your target (step 3). The salary split (step 1) and the debt/equity/gold split are simple stacked bars in HTML (`bar3()`); the emergency buffer is an SVG gauge (0–6 months, 3-month marker) and goal progress an SVG ring. Chart colours (Steady blue, Balanced orange, Growth green) were checked for colour-blind safety on white. |
| 7 | Top bar and step tabs | Logo ("White." with the navy full stop), AI on/off toggle, and the step row: a `st.segmented_control` whose labels are numbered with `format_func`; `nav_changed()` keeps it in sync with the Back/Next buttons. On phones the top bar also shows four progress dots (`progress_html()`). |
| 8–12 | The five screens | Welcome → Where I stand (tabbed inputs; hero "free this month" with salary bar, 4 KPI tiles, buffer gauge) → Set a goal (goal-type pills, goal card with progress ring and On track / Behind pill, pace chart) → Investment options (3 risk questions as segmented choices, goal-date range chart, 3 option cards each with a "Choose" button that sets `S.choice` through `pick()`) → My plan (plan card, "What if…?" with a before → after timeline, download). Desktop: inputs left, results right. |
| 12 | "What if…?" check (in step 4) | The user enters a one-off spend or a change to the monthly amount. The same `months_to_goal()` rule recalculates the goal date and the buffer before and after; Gemini explains the trade-off without saying whether to do it. |

## Why the AI is designed this way (link to your research)
- **Rules calculate, AI explains**: numbers must be correct and repeatable; language models can make arithmetic mistakes.
- **AI never picks an option**: research respondents wanted to keep the final decision.
- **Only summary numbers are sent**: privacy concerns from interviews and the Reddit thread.
- **Works without AI**: graceful fallback, and the user can turn AI off.

## Things to try changing yourselves (good for "debug and iterate")
- Change the three mixes in `MIXES` (section 5).
- Edit the rules in `SYSTEM_PROMPT` (section 4) and see how the explanation changes.
- Change sample numbers in `DEFAULTS` (section 3) to match your persona.
- Change the colours in `:root` (section 1) or in `.streamlit/config.toml`; the brand accent is `#14213D`, gold `#B8862B` is reserved for the AI card.
- If Gemini says the model is not found, set `GEMINI_MODEL = "gemini-2.5-flash"` (or a current model name from aistudio.google.com) in secrets.
