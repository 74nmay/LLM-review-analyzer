import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from pymongo import MongoClient
from groq import Groq  # <--- NEW IMPORT
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- 1. CONFIGURATION ---

MONGO_URI = os.getenv("MONGO_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Setup Database
client = MongoClient(MONGO_URI)
db = client.feedback_system
reviews_collection = db.reviews

# Setup Groq Client
client_groq = Groq(api_key=GROQ_API_KEY)

# Setup Frontend Templates
templates = Jinja2Templates(directory="templates")

# --- 2. THE AI FUNCTION (GROQ VERSION) ---
def analyze_with_ai(review_text, stars):
    """Sends the review to Groq (Llama 3) for analysis."""
    try:
        prompt = f"""
        You are a customer experience manager. Analyze this review:
        Rating: {stars}/5
        Review: "{review_text}"
        
        Output a response in this exact format (keep it short):
        SUMMARY: (A 5-word summary of the issue)
        ACTION: (One specific step the business should take)
        REPLY: (A polite, empathetic message to the customer)
        """
        
        completion = client_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            # We use Llama 3 (Free & Fast on Groq)
            model="llama-3.3-70b-versatile",
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Groq AI Call Failed: {e}")
        return "SUMMARY: N/A\nACTION: Check manually\nREPLY: Thank you for your feedback."

# --- 3. THE WEBPAGES (No changes here) ---

@app.get("/", response_class=HTMLResponse)
async def user_form(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_review(request: Request, stars: int = Form(...), review: str = Form(...)):
    # A. Call AI
    ai_output = analyze_with_ai(review, stars)
    
    # B. Extract Reply
    user_reply = "Thank you!"
    if "REPLY:" in ai_output:
        parts = ai_output.split("REPLY:")
        if len(parts) > 1:
            user_reply = parts[1].strip()

    # C. Save to DB
    doc = {
        "stars": stars,
        "review": review,
        "ai_full_analysis": ai_output,
        "timestamp": datetime.now()
    }
    reviews_collection.insert_one(doc)

    return templates.TemplateResponse("user.html", {
        "request": request, 
        "success": True, 
        "ai_message": user_reply
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    reviews = list(reviews_collection.find().sort("timestamp", -1))
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "reviews": reviews
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)