# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IncidentRequest(BaseModel):
    type: str

@app.post("/chat")
async def chat(req: IncidentRequest):
    try:
        prompt = f"""
You are a cybersecurity assistant helping system administrators.
You must only answer questions strictly related to cybersecurity, such as threat response, mitigation strategies, incident handling, and best practices.
Do not respond to questions outside the cybersecurity domain. If a question is unrelated, respond with:
"I'm here to help with cybersecurity-related topics only."


{req.type}
"""
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
