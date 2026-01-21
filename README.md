# LLM Review Analyzer

A real-time customer feedback system powered by **FastAPI** and **Groq (Llama 3)**. This application collects user reviews, instantly analyzes them using AI to generate actionable business insights, and provides an auto-generated empathetic response.

**Live Demo:** [https://llm-review-analyzer.onrender.com/](https://llm-review-analyzer.onrender.com/)

**Admin Dashboard:** [https://llm-review-analyzer.onrender.com/admin](https://llm-review-analyzer.onrender.com/admin)

---

## Features

* **AI-Powered Analysis:** Uses Groq's `llama-3.3-70b-versatile` model to analyze sentiment and content instantly.
* **Structured Insights:** Automatically categorizes feedback into three distinct outputs for the admin:
* **SUMMARY:** A 5-word summary of the issue.
* **ACTION:** A specific step the business should take.
* **REPLY:** A polite, empathetic message draft for the customer.


* **Real-time Database:** Stores ratings, reviews, and AI analysis in **MongoDB Atlas**.
* **Dual Interface:**
* **User Interface:** Clean Bootstrap-based form for submitting reviews.
* **Admin Dashboard:** Dedicated view to monitor live feedback and AI suggestions.



---

## Tech Stack

* **Backend Framework:** FastAPI
* **Server:** Uvicorn
* **LLM Engine:** Groq API (Llama 3)
* **Database:** MongoDB (Pymongo)
* **Templating:** Jinja2
* **Frontend:** HTML5, Bootstrap 5.3

---

## Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/74nmay/LLM-review-analyzer.git
cd LLM-review-analyzer

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add your keys (required by `main.py`):

```env
MONGO_URI="your_mongodb_connection_string"
GROQ_API_KEY="your_groq_api_key"

```

### 4. Run the Application

Start the server using Uvicorn:

```bash
uvicorn main:app --reload

```

The app will be available at `http://127.0.0.1:8000`.

---

## Project Structure

```text
├── main.py              # Application entry point & API routes
├── database.py          # MongoDB connection utility
├── templates/
│   ├── user.html        # Customer review submission form
│   └── admin.html       # Admin dashboard for viewing analysis
├── requirements.txt     # Python dependencies
├── Procfile             # Render deployment command
└── README.md

```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Renders the customer feedback form. |
| `POST` | `/submit` | Accepts form data, triggers Groq AI analysis, saves to MongoDB. |
| `GET` | `/admin` | Displays a table of all reviews and their AI insights. |

---

## Deployment

This project is configured for deployment on **Render**.

1. Connect your GitHub repository to Render.
2. Set the **Build Command**: `pip install -r requirements.txt`
3. Set the **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add your `MONGO_URI` and `GROQ_API_KEY` in the Render Environment settings.
