# EduGenie — Google Gemini Powered Learning Assistant

Complete FastAPI + HTML/CSS/JavaScript project implementing the five workflows in the supplied documentation: Q&A, simple explanations, 3-question MCQ quizzes, summaries, and personalized learning roadmaps.

## Prerequisites
Python 3.10+ (3.11 recommended), VS Code, internet access, and a Gemini API key from https://aistudio.google.com/api-keys.

**Security:** The provided PDF contains a string that looks like an API credential. Do not use or publish it. If it is a real key, revoke it and create a fresh key. Keep your key only in `.env`; never in frontend files or Git.

## Windows + VS Code setup
1. Install Python and the VS Code Python extension.
2. Extract the ZIP and open the `EduGenie` folder in VS Code.
3. Terminal → New Terminal:
   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   If activation is blocked, use Command Prompt and run `.venv\Scripts\activate.bat`.
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Create your environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env` and replace `PASTE_YOUR_KEY_HERE` with your own key.
6. Run:
   ```powershell
   uvicorn main:app --reload
   ```
7. Open http://127.0.0.1:8000. API testing docs: http://127.0.0.1:8000/docs.

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set your Gemini key
uvicorn main:app --reload
```

## Test the application
- `http://127.0.0.1:8000/health` should show status `ok` and `api_key_configured: true`.
- Test all five tasks through the home page.
- Use `/docs` to POST JSON to each endpoint. Example:
  `{"text":"Explain photosynthesis","level":"Beginner"}`
- Run smoke tests: `pytest -q`.

## Endpoints
`POST /qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`. JSON input: `text` and optional `level`. Quiz result is a list of three questions, each with four options, answer, and explanation.

## Model note
The PDF refers to Gemini 1.5 Pro and LaMini-Flan-T5-783M. Legacy model access and local model downloads may vary. This implementation uses Google's current `google-genai` SDK and defaults to `gemini-2.5-flash`; change `GEMINI_MODEL` in `.env` to a model available to your AI Studio account. Explanation is also routed through Gemini to avoid a large local model download and simplify setup on student laptops. AI output may contain errors; verify important facts with course materials.
