import os,json,re,asyncio,logging
from google import genai
from google.genai import types
log=logging.getLogger(__name__)
class AIServiceError(Exception): pass

class EduGenieAI:
    def __init__(self):
        key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model=os.getenv("GEMINI_MODEL","gemini-2.5-flash")
        self.client=genai.Client(api_key=key) if key else None
    @property
    def configured(self): return self.client is not None

    def prompt(self,task,text,level):
        base="You are EduGenie, a careful educational tutor. Explain clearly, avoid unsupported claims, and use age-appropriate language.\n"
        p={
        "qa":f"Answer the student's question concisely and include an example if helpful: {text}",
        "explain":f"Explain this concept for a {level} learner in simple language. Give a definition, steps, and example: {text}",
        "summarize":f"Summarize this educational text in plain language, preserving key facts and terms. Add key points: {text}",
        "recommend":f"Make a structured beginner-to-advanced learning roadmap for {text} for a {level} learner. Include sequence, milestones, practice tasks, and resource types. Do not invent URLs.",
        "quiz":f"Create exactly 3 MCQs from the topic/passage. Each has exactly four options, one correct answer, and a brief explanation. Return ONLY JSON array objects with keys question, options (four strings), answer (exact option string), explanation. Content: {text}"
        }
        return base+p[task]

    async def generate(self,task,text,level):
        if not self.client: raise AIServiceError("Missing Gemini API key. Add GEMINI_API_KEY to .env.")
        try:
            response=await asyncio.to_thread(self.client.models.generate_content,model=self.model,contents=self.prompt(task,text,level),config=types.GenerateContentConfig(temperature=0.4))
            answer=(response.text or "").strip()
            if not answer: raise AIServiceError("Gemini returned an empty response.")
            if task=="quiz":
                answer=re.sub(r"^```(?:json)?\s*|\s*```$","",answer,flags=re.I).strip()
                data=json.loads(answer)
                if not isinstance(data,list) or len(data)!=3: raise AIServiceError("Quiz output must contain three questions.")
                for q in data:
                    if len(q.get("options",[]))!=4 or q.get("answer") not in q["options"]: raise AIServiceError("Invalid quiz structure; please retry.")
                return {"task":task,"result":data}
            return {"task":task,"result":answer}
        except AIServiceError: raise
        except json.JSONDecodeError: raise AIServiceError("Gemini returned malformed quiz JSON. Please retry.")
        except Exception as e:
            log.exception("Gemini call failed")
            msg=str(e).lower()
            if "429" in msg or "quota" in msg: raise AIServiceError("Gemini quota or rate limit reached. Check AI Studio usage and retry later.")
            if "api key" in msg or "unauthorized" in msg: raise AIServiceError("Gemini rejected the API key. Verify it in Google AI Studio.")
            raise AIServiceError("Gemini request failed. Check internet, API key, and model availability.")
