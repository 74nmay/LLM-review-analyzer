import os
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from pymongo import MongoClient
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# --- Configuration ---
MONGO_URI = os.getenv("MONGO_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database connection
client = MongoClient(MONGO_URI)
db = client.feedback_system
reviews_collection = db.reviews

# AI Client connection
client_groq = Groq(api_key=GROQ_API_KEY)

# Template directory
templates = Jinja2Templates(directory="templates")

# --- Helper Functions ---
def analyze_with_ai(review_text, stars):
    """
    Sends the review text and rating to the Groq API (Llama 3) to generate
    a structured summary, action item, and customer reply.
    """
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
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"AI Service Error: {e}")
        return "SUMMARY: N/A\nACTION: Manual review required\nREPLY: Thank you for your feedback."

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def user_form(request: Request):
    """Renders the customer review submission form."""
    return templates.TemplateResponse("user.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_review(request: Request, stars: int = Form(...), review: str = Form(...)):
    """
    Handles form submission. Validates input, calls AI for analysis,
    saves data to MongoDB, and returns the success page.
    """
    # Validation: Ensure review is not empty
    if not review.strip():
        return templates.TemplateResponse("user.html", {
            "request": request, 
            "error": "Review cannot be empty. Please share your experience."
        })

    # AI Analysis
    ai_output = analyze_with_ai(review, stars)
    
    # Parse the 'REPLY' section for the user
    user_reply = "Thank you for your feedback!"
    if "REPLY:" in ai_output:
        parts = ai_output.split("REPLY:")
        if len(parts) > 1:
            user_reply = parts[1].strip()

    # Save to MongoDB
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
    """
    Renders the admin dashboard with live analytics and review history.
    """
    # Fetch all reviews sorted by newest first
    reviews = list(reviews_collection.find().sort("timestamp", -1))
    
    # Calculate Analytics
    total_reviews = len(reviews)
    average_rating = 0.0
    star_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    
    if total_reviews > 0:
        total_stars = 0
        for r in reviews:
            s = r.get("stars", 0)
            if s in star_counts:
                star_counts[s] += 1
            total_stars += s
        average_rating = round(total_stars / total_reviews, 1)

    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "reviews": reviews,
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "star_counts": star_counts
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
