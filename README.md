# White · save now, spend later

DPM 2026 · IIM Visakhapatnam EMBA · Group 9 · Phase 2 interactive prototype (Streamlit + Gemini)

**Live app:** https://white-dpm.streamlit.app  ·  **Code:** https://github.com/Akhil-1/white  ·  **Problem space:** simplifying how individuals track, manage and make better financial decisions

## The product in one paragraph

On salary day, a salaried professional saving for one goal (a car, a home deposit, a trip) has all the data and none of the decision. Bank apps show the past; investment apps sell the next product. White is a 10-minute salary-day check-in: it shows what is free this month, how far the goal is, what each saving mix does to the goal date, and what a one-off spend would change, **before** the money moves. Fixed rules do every calculation. Gemini only explains the trade-off in plain words, and the user can see exactly what is sent to it.

| | |
|---|---|
| **User** | Salaried, 23–35, manages their own money, saving for a dated goal (persona: Meera, 32, Hyderabad) |
| **Problem** | "Can I buy this and still be on time for my goal?" No app answers it this month, in rupees |
| **One workflow** | Where I stand → Set a goal → Investment options → My plan + "What if…?" |
| **One AI capability** | Explain the trade-off between options using only the calculated facts |
| **Not in scope** | Bank linking, fund names, "best option" advice, login, a server database |

## What the prototype does

0. **Salary-day home.** The top card slides with **Next**: what is free this month, then one coloured card per goal showing what is left after it (the sample has a ₹8 lakh car and a ₹3 lakh Europe trip in 4 years: ₹38,400 → ₹20,400 → ₹15,400). Below, a card for every goal: % saved, where today's salary takes it, a small chart of your pace against the on-time line, the date at this pace and what is needed per month to be on time. **"I've put aside ₹18,000"** and **Lump sum** can be used any day, as often as money goes in; the goal moves forward, the check-in is saved in this browser, and the last addition can be undone. Amounts are typed with Indian commas (1,45,000). On a phone the three investment options swipe sideways instead of stacking.
   - **"Thinking of buying something?"** on Home: type an amount, choose free money or goal money, and see the effect at once (free money left, or how many days or months later the goal lands), without the full check-in.
   - Each goal card lists the **months put aside** so far, and has **Update value**: if the goal money is invested (a fund, RD or FD), type what it's worth today and White re-plans from it. Nothing is linked.
   - **Payday runway:** the month from salary to salary as a chart: goal money out first, rent, EMIs, SIPs and bills on their due days, daily spending spread evenly. It shows what's left today, the biggest hit and what is truly spare per day.
   - **Since last month:** chips flag what changed since the previous month's check-in, e.g. "Daily spending ↑ ₹3,000".
1. **Where I stand.** Income, fixed monthly expenses (rent, EMIs, SIPs, bills), regular daily spending and savings. Shows what is free this month and how many months the emergency buffer covers.
2. **Set a goal.** One or more goals, each with a cost, a target date and what is already saved. Shows the amount needed per month to be on time, and a pace chart. A goal tracker appears on the welcome screen.
3. **Investment options.** Your timeline comes first: the goal date decides what is sensible (under 3 years mostly debt, 3–5 years balanced, over 5 years equity can recover), so the matching mix is labelled **Timeline match** (an illustrative rule of thumb, not personalised advice) and chosen by default. Three short questions set your stated comfort. A one-line trade-off shows how many months equity saves against what one bad year could cost. Three mixes (Steady 85/5/10, Balanced 40/50/10, Growth 10/85/5, as debt/equity/gold) each show:
   - the expected goal date, and the date if markets are weak;
   - the amount needed per month to be on time;
   - the rupee fall in a bad year;
   - whether it fits your timeline and your stated comfort.
4. **My plan.** It opens with a verdict, "This plan works" or "This plan doesn't work yet", and the reason in rupees and months. Below it, every realistic plan sits side by side: your numbers, keep the date, move the date, lower the cost, and put aside all that's free (or spend less). **Preview** any of them and the whole page shows that plan; nothing changes until you press **Use this plan**, and **Back to my numbers** undoes the preview. The assumed returns are debt 7%, equity 15% and gold 8% a year, all editable.
   - **The plan:** the chosen mix and where the goal money sits (debt, equity, gold), kept apart from the emergency buffer.
   - **"What if…?":** shows what a one-off spend does to the goal date and the buffer.
   - **"Tune your plan":** update what the goal money is worth today, the monthly amount, the target or the mix; the plan and an On track / N months behind verdict update live.
   - **"Remind me every salary day":** a calendar file (Google, Outlook, Apple) with a monthly reminder on the salary date.

The app works without a Gemini key: every AI card falls back to a rule-based sentence.

**AI only when asked.** Each card shows the rule-based sentence at once, with an **Explain with AI** button. Gemini is called only when you press it, and again only if you press **Update AI explanation** after changing numbers, so dragging a slider never triggers a call. Answers are cached, so returning to the same numbers costs nothing.

**Clear all goals** (on Home and on Set a goal) removes the sample goal and every other goal, and starts you on a blank one.

**Start fresh** (on Home) and **Clear all numbers and goals** (on Where I stand) set every amount to zero and remove all goals, so you can enter your own numbers. A clean start is remembered in the browser across reloads until you save a real check-in.

## See it work (simulation)

At the bottom of My plan, "See it work" plays the next 6–36 salary days forward in three markets (Calm, Crash in year 1, Bumpy) for all three mixes on the same market path. A chart shows the gain or loss against the money put in, a table compares the end value, lowest point and goal date per mix, and dated check-in cards show what White would tell you at each one: on plan, below plan but on time, or behind with the one-off top-up that would get you back on plan. The mixes are 85/5/10 (Steady), 40/50/10 (Balanced) and 10/85/5 (Growth), as debt/equity/gold.

## Ask White

A chat button pinned to the bottom-right of every screen. It answers from the person's own numbers, e.g. "Can I afford a ₹15,000 phone?", "What if my salary is 5 days late?", "Am I behind on my goal?". It works without AI, with calculated answers; with a Gemini key it rephrases them. It never picks a product.

## Input style

Every amount has a slider and a number box that stay in sync: drag for speed, type for precision. The goal date has a "months from now" slider next to the calendar.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your Gemini key
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a public GitHub repo. `.streamlit/secrets.toml` is git-ignored, so the key is never uploaded.
2. On share.streamlit.io choose **Create app**, pick the repo, branch `main`, file `app.py`.
3. In **Advanced settings → Secrets** paste `GEMINI_API_KEY = "your-key"`.
4. Deploy. You only need the key: the app uses `gemini-flash-latest` and falls back to other current Flash models on its own. If a card says "AI unavailable", the reason is shown in brackets.

## Files

| File | Purpose |
|---|---|
| `app.py` | The whole app: styling, rules, the five screens, the Gemini call and the plan Q&A |
| `requirements.txt` | Packages Streamlit Cloud installs (pinned to major versions) |
| `HOW_IT_WORKS.md` | Section-by-section notes for explaining the code in class |
| `.streamlit/config.toml` | Light theme for native widgets |
| `.streamlit/secrets.toml.example` | Template for the Gemini key |

## Privacy and limits

- No login, no bank connection, no server database. Inputs live in the browser session.
- "Save this month's check-in" keeps a summary in that browser's local storage only; "Clear history" removes it.
- Gemini receives only summary numbers and the user's question, never names, account numbers or transactions. Each AI card has a "What's sent to the AI" panel showing the exact data.
- The returns are editable planning assumptions, not forecasts. FD and loan interest are not projected. White does not name funds or recommend a product; it is not investment advice.
