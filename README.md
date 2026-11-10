# White. · your money, nothing hidden

DPM 2026 · Group 9 · Phase 2 prototype (Streamlit + Gemini)

> **Group: replace this section with your own product description** (problem, user, value).
> The sections below are technical setup notes only.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your Gemini key
streamlit run app.py
```

The app also works without a key: AI explanations are replaced by calculation-only text.

## Deploy on Streamlit Community Cloud

1. Push this folder to a **public GitHub repo** (`.streamlit/secrets.toml` is git-ignored, so your key is not uploaded).
2. Go to share.streamlit.io, sign in with GitHub, choose **Create app**, pick the repo, branch `main`, file `app.py`.
3. In **Advanced settings → Secrets**, paste:
   ```
   GEMINI_API_KEY = "your-key"
   ```
4. Deploy. The public URL is the live link for the slides.
5. If Gemini reports the model is not found, add `GEMINI_MODEL = "gemini-2.5-flash"` to the secrets (the app also tries this automatically once).

## Files

| File | Purpose |
|---|---|
| `app.py` | The whole app: styling, calculations, the 4-step flow and the Gemini call |
| `requirements.txt` | Python packages Streamlit Cloud installs (pinned to major versions) |
| `HOW_IT_WORKS.md` | Section-by-section notes for explaining the code in class |
| `.streamlit/config.toml` | Light theme (colours, fonts, radius) that native widgets use |
| `.streamlit/secrets.toml.example` | Template for the Gemini key |

## Privacy

No login, no database, no bank connection. Inputs live only in the browser session.
Only summary numbers (shown in the app under "What's sent to the AI") are sent to Gemini.
