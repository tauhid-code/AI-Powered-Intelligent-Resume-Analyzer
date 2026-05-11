#  Hirelytics AI — Resume Intelligence Platform

> **An end-to-end AI-powered platform that scores resumes against job descriptions using a custom ATS engine, extracts skill gaps, and generates personalized interview questions using a Large Language Model.**

<br/>

##  Demo Video

[![Watch Demo](https://img.shields.io/badge/▶%20Watch%20Demo-Google%20Drive-red?style=for-the-badge&logo=google-drive)](https://drive.google.com/file/d/1TL-Q3UIMuibFVwpk3Xw0n4jvcAYso-kN/view?usp=sharing)

> Click the badge above to watch a full walkthrough of the platform in action.

<br/>

---

##  Project Goal

The goal of Hirelytics AI is to solve a real-world problem that every job seeker faces — **not knowing why their resume gets rejected by ATS (Applicant Tracking Systems)** before a human even reads it.

Most candidates apply to jobs without understanding how ATS software filters resumes based on keyword matching, semantic relevance, and structural completeness. This platform gives candidates the same intelligence that recruiters use — helping them optimize their resume for any specific job description before applying.

Beyond scoring, the platform also acts as an **AI Interview Coach** — generating role-specific technical, behavioral, and project-based interview questions based on the candidate's actual resume analysis.

<br/>

---

##  Features

###  ATS Resume Scoring Engine
- Upload a PDF resume and paste any Job Description
- Get an overall **ATS Score (0–100)** with detailed breakdown
- Three sub-scores: Keyword Match, Semantic Similarity, Section Coverage
- Visual score ring with color-coded performance labels

###  Skill Gap Analysis
- Extracts and compares skills from resume vs JD using a **200+ skill taxonomy** across 13 categories
- Shows **Matched Skills** (green chips) and **Missing Skills** (red chips)
- Fuzzy matching handles variations like "nodejs" vs "node.js"
- Actionable improvement tips based on gap analysis

###  Analysis History
- Stores last 5 resume analyses per session
- Each entry shows ATS score, keyword score, semantic score, section coverage
- Expandable cards with full skill breakdown and JD preview

###  AI Interview Coach
- Select any saved analysis from history
- Enter your target role
- Generates **4 categories of interview questions** using Groq LLM (llama-3.1-8b-instant):
  - **Technical Questions** (Medium–Hard, from matched skills) with model answers
  - **Gap Questions** (Easy–Medium, from missing skills) with beginner-friendly answers
  - **Project Deep-Dive** (4 questions with difficulty levels + project summary)
  - **Behavioral Questions** (3 scenario-based questions)
- Toggle "Show Answer" for each question

###  Authentication System
- Secure user registration and login
- **JWT-based authentication** with configurable token expiry
- **bcrypt password hashing** — plain passwords never stored
- Session persistence across page navigation

<br/>

---

##  How the ATS Scoring Works

The scoring pipeline combines three independent signals into one weighted final score:

```
ATS Score = (0.50 × Keyword Match Score)
          + (0.25 × Semantic Similarity Score)
          + (0.25 × Section Coverage Score)
```

| Component | Weight | How It's Calculated |
|---|---|---|
| **Keyword Match** | 50% | Skill taxonomy regex extraction → intersection of resume skills vs JD skills |
| **Semantic Similarity** | 25% | Sentence embeddings (all-MiniLM-L6-v2) → cosine similarity of resume vs JD text |
| **Section Coverage** | 25% | Regex detection of Skills, Experience, Projects sections in resume |

### Skill Extraction Pipeline
1. Regex pattern matching against **200+ curated skills** across 13 categories
2. RapidFuzz fuzzy matching (85% threshold) for spelling variations
3. Skills categorized into: Programming Languages, Web Frameworks, ML/AI, Data Engineering, Cloud, DevOps, Databases, Visualization, Version Control, Soft Skills, Methodologies, Testing, Security

<br/>

---

##  Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **SQLite** | User database |
| **JWT (PyJWT)** | Authentication tokens |
| **bcrypt** | Password hashing |
| **Pydantic** | Request/response validation |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|---|---|
| **Streamlit** | Multi-page web application |
| **Custom CSS** | Dark theme UI (#0e1117 palette) |
| **HTML components** | Cards, chips, score rings, banners |

### AI / ML Pipeline
| Technology | Purpose |
|---|---|
| **sentence-transformers** | Semantic similarity (all-MiniLM-L6-v2) |
| **PyTorch** | Embedding model runtime |
| **scikit-learn** | Cosine similarity computation |
| **RapidFuzz** | Fuzzy skill matching |
| **NLTK** | Text preprocessing |
| **Groq API (llama-3.1-8b-instant)** | LLM interview question generation |

### Document Processing
| Technology | Purpose |
|---|---|
| **PyMuPDF (fitz)** | PDF text extraction |
| **pdfplumber** | Fallback PDF parsing |

<br/>

---

##  Project Architecture

```
AI-Resume Intelligence/
│
├── backend/                        # FastAPI backend
│   ├── main.py                     # App entry point, CORS, middleware
│   ├── auth.py                     # Login & signup endpoints
│   ├── database.py                 # SQLite init & connection
│   ├── models.py                   # Pydantic request/response models
│   ├── dependencies.py             # JWT auth dependency injection
│   └── utils/
│       └── security.py             # JWT creation & verification
│
├── src/                            # Core AI/ML pipeline
│   ├── scorer.py                   # ATS scoring orchestrator
│   ├── skills_extractor.py         # Skill taxonomy + extraction + fuzzy match
│   ├── parser.py                   # PDF resume parser
│   ├── preprocessing.py            # Text cleaning & tokenization
│   ├── utils.py                    # Cosine similarity, section detection
│   └── interview_coach.py          # Groq LLM question generation
│
├── frontend/                       # Streamlit application
│   ├── app.py                      # Entry point
│   ├── login.py                    # Authentication page
│   ├── pages/
│   │   └── home.py                 # Dashboard, Analysis, Interview Coach
│   └── components/
│       └── sidebar.py              # Navigation sidebar component
│
├── uploads/
│   └── resumes/                    # Uploaded PDF storage
│
├── data/
│   └── ai_resume_intelligence.db   # SQLite database
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
└── README.md
```

<br/>

---

##  Local Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/ai-resume-intelligence.git
cd ai-resume-intelligence
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure environment variables
Create a `.env` file in the root directory:
```env
# JWT Security
SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DB_PATH=data/ai_resume_intelligence.db

# API URL
API_BASE_URL=http://localhost:8000

# Groq API (get your free key at https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Step 4 — Run the backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### Step 5 — Run the frontend (open a new terminal)
```bash
cd frontend
streamlit run app.py
```

### Step 6 — Open in browser
```
http://localhost:8501
```

<br/>

---

##  Environment Variables Reference

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | JWT signing secret key | ✅ |
| `JWT_ALGORITHM` | Algorithm for JWT (default: HS256) | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration in minutes | ✅ |
| `DB_PATH` | Relative path to SQLite database | ✅ |
| `API_BASE_URL` | FastAPI server base URL | ✅ |
| `GROQ_API_KEY` | Groq API key for LLM features | ✅ |
| `GROQ_MODEL` | Groq model name | ✅ |

<br/>

---

## 📈 ATS Score Interpretation

| Score Range | Label | Meaning |
|---|---|---|
| 80 – 100 | 🟢 Excellent | Strong match — highly likely to pass ATS filters |
| 60 – 79 | 🟡 Good | Good match — minor keyword improvements needed |
| 40 – 59 | 🟠 Fair | Moderate match — significant skill gaps present |
| 0 – 39 | 🔴 Poor | Weak match — resume needs major restructuring |

<br/>

---

##  Application Pages

| Page | Description |
|---|---|
| **Login / Sign Up** | JWT-secured authentication with bcrypt password hashing |
| **Dashboard** | Upload resume, paste JD, run ATS analysis, view live results |
| **Analysis History** | Last 5 analyses with full score breakdown and skill gap chips |
| **AI Interview Coach** | Select any past analysis, enter target role, generate LLM questions |

<br/>

---

##  Core Dependencies

```
fastapi==0.111.0
streamlit==1.35.0
sentence-transformers==2.7.0
torch==2.3.1
scikit-learn==1.5.0
groq
PyMuPDF==1.24.9
pdfplumber==0.1.0
python-jose==3.5.0
bcrypt==4.1.2
rapidfuzz
python-dotenv==1.0.1
pydantic==2.7.1
uvicorn==0.29.0
```

<br/>

---

##  About This Project

This project was built as a full-stack AI portfolio project demonstrating real-world skills across the entire development stack:

- **Backend Engineering** — REST API design, JWT authentication, SQLite database, security best practices
- **Machine Learning** — NLP pipelines, sentence embedding models, custom scoring algorithms, fuzzy matching
- **LLM Integration** — Prompt engineering, structured JSON generation from LLMs, Groq API
- **Frontend Development** — Multi-page Streamlit application, custom dark-theme UI with HTML/CSS components
- **System Design** — Multi-service architecture (separate frontend & backend), component-based code structure

<br/>

---

##  License

This project is built for educational and portfolio purposes.

---

<div align="center">
  <strong>Built using FastAPI · Streamlit · Groq · sentence-transformers · PyTorch</strong>
</div>
