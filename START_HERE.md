# Start here: running White. on a new computer

There are two ways. **Option A needs nothing installed**: you only need a browser. Option B runs the app on your own laptop.

---

## Option A · Put it online (no installs, about 15 minutes)

You need: a GitHub account (free) and a Google account (for the Gemini key).

**1. Create the GitHub repo**
1. Go to github.com and sign up or sign in.
2. Click **+** (top right) → **New repository**.
3. Name it `white-app`, choose **Public**, tick **Add a README file**, then click **Create repository**.

**2. Upload the app files**
1. Unzip `white-app-v6.zip` on your computer.
2. In the repo, click **Add file → Upload files**.
3. Open the unzipped folder, select **everything inside it**, and drag it onto the page:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `HOW_IT_WORKS.md`
   - `START_HERE.md`
4. Upload the `.streamlit` folder as well. Hidden folders can be tricky: if you can't see it, turn on hidden files.
   - Windows: File Explorer → View → Show → Hidden items.
   - Mac: in Finder press Cmd + Shift + .
   - If it still won't upload, skip it. The app still works; only the theme colours of a few native widgets differ slightly.
5. Click **Commit changes**. If GitHub asks to replace its README, allow it.

**3. Get a Gemini key (free)**
1. Go to aistudio.google.com and sign in with Google.
2. Click **Get API key → Create API key**, then copy it.
3. Keep it private. Never paste it into GitHub or the slides.

**4. Deploy on Streamlit Community Cloud**
1. Go to share.streamlit.io and click **Continue with GitHub**. Allow access.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Repository: `your-username/white-app` · Branch: `main` · Main file path: `app.py`.
4. Optional: choose an App URL, e.g. `white-dpm-gr9`.
5. Click **Advanced settings**. In **Secrets**, paste the line below with your key:
   ```
   GEMINI_API_KEY = "paste-your-key-here"
   ```
6. Click **Deploy**. The first start takes 2–4 minutes. The link it gives you is your live app link for the slides.

**Updating later.** In GitHub, open `app.py` → pencil icon → paste the new code → **Commit**. The live app refreshes on its own within a minute.

**If something goes wrong**
- *"AI unavailable" on the cards:* the key is missing or wrong. Fix it in Streamlit → your app → **⋮ → Settings → Secrets**. The app still works without AI.
- *"Model not found":* add a second line to Secrets: `GEMINI_MODEL = "gemini-2.5-flash"`.
- *"ModuleNotFoundError":* `requirements.txt` was not uploaded. Upload it, and the app rebuilds.

---

## Option B · Run it on your own laptop

**1. Install Python (once)**
- **Windows:** download Python 3.12 from python.org/downloads. In the installer, **tick "Add python.exe to PATH"**, then click Install Now.
- **Mac:** download Python 3.12 from python.org/downloads and install it.

**2. Open a terminal in the app folder**
1. Unzip `white-app-v6.zip`.
2. Open a terminal in that folder:
   - **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
   - **Mac:** right-click the folder → **New Terminal at Folder**. If that's missing, open Terminal, type `cd ` and drag the folder in.

**3. Install and run (copy one line at a time)**

Windows:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Mac:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The browser opens at `http://localhost:8501`. To stop the app, press **Ctrl + C** in the terminal.

**4. Turn on the AI explanations (optional)**
1. In the `.streamlit` folder, copy `secrets.toml.example` and rename the copy `secrets.toml`.
2. Open it in Notepad or TextEdit and paste your key between the quotes.
3. Save, then restart the app.

**Already installed an earlier version?** Run `pip install -r requirements.txt` once more after activating. The app now pins exact versions (Streamlit 1.67.0), and a newer Streamlit draws some buttons differently.

**If pip shows a long red error mentioning pandas, meson or Visual Studio:** run `python -m pip install --upgrade pip`, then `pip install --prefer-binary -r requirements.txt`. If it still fails, install Python 3.12 from python.org and start again with a fresh folder.

**Next time** you only need two commands: the activate line (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` on Mac), then `streamlit run app.py`.

---

## A 1-minute tour for the demo
1. **Home:** what's free this month, and each goal's card. Press **I've put aside ₹18,000** to tick the month off.
2. **Start check-in → Where I stand:** income, fixed expenses, savings.
3. **Set a goal:** cost, date and what's saved; add more goals if you like.
4. **Investment options:** three questions, then three mixes with dates, ₹ by the target date and the bad-year fall.
5. **My plan:** try **What if…?** with ₹15,000 and **Ask about your plan**.

Sample numbers are pre-filled, so the demo works straight away.
