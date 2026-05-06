# ⟨/⟩ CodeSphere

A cloud-based Online Compiler & Coding Judge Platform built with FastAPI, Monaco Editor, Docker, and deployable on AWS.

---

## 🗂️ Project Structure

```
codesphere/
├── frontend/               # Static HTML/CSS/JS (deploy on AWS Amplify)
│   ├── index.html          # Landing page
│   ├── problems.html       # Problem list
│   ├── problem-detail.html # Problem + Monaco editor + Judge
│   ├── playground.html     # Free code execution
│   ├── css/main.css        # All styles (dark/light themes)
│   └── js/app.js           # API client, auth, toast, modals
│
├── backend/                # FastAPI (deploy on AWS EC2)
│   ├── main.py             # App entry point + CORS
│   ├── database.py         # SQLAlchemy + SQLite setup
│   ├── models.py           # User, Problem, Submission, PlaygroundRun
│   ├── judge.py            # Docker execution engine
│   ├── routes/
│   │   ├── auth.py         # POST /register, POST /login, GET /me
│   │   ├── problems.py     # GET /problems, GET /problem/{id}
│   │   └── judge.py        # POST /run, POST /submit, GET /result/{id}
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker/                 # Sandboxed execution images
    ├── python/Dockerfile   → codesphere-python
    ├── cpp/Dockerfile      → codesphere-cpp
    └── java/Dockerfile     → codesphere-java
```

---

## 🚀 Local Development Setup

### 1. Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

The API will be at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

### 2. Docker Execution Images (required for code running)

```bash
# From project root
chmod +x build-docker.sh
./build-docker.sh
```

> **Without Docker**, the judge falls back to direct execution using system-installed Python/GCC/Java. This is fine for development.

### 3. Frontend

Open any HTML file directly in your browser, or serve with:
```bash
cd frontend
python3 -m http.server 3000
```

Then open `http://localhost:3000`.

> **Important**: Update `API_BASE` in `js/app.js` to point to your backend URL:
```javascript
const API_BASE = window.API_BASE || 'http://localhost:8000';
```

---

## ☁️ AWS Deployment

### Frontend → AWS Amplify

1. Push `frontend/` folder to a GitHub repo
2. In AWS Amplify → New App → Connect to GitHub
3. Set build settings (no build needed — static files)
4. Deploy — auto-builds on every push

### Backend → AWS EC2

```bash
# On EC2 (Ubuntu 22.04)
sudo apt update && sudo apt install -y python3-pip python3-venv docker.io git

# Clone repo
git clone <your-repo>
cd codesphere/backend

# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Build Docker images
cd .. && ./build-docker.sh

# Run with uvicorn (production)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Or use screen/tmux to keep running:
screen -S codesphere
uvicorn main:app --host 0.0.0.0 --port 8000
# Ctrl+A D to detach
```

Don't forget to:
- Open port 8000 in EC2 Security Group
- Update `API_BASE` in `frontend/js/app.js` to your EC2 public IP/domain

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Create account | No |
| POST | `/login` | Login, get JWT token | No |
| GET | `/me` | Get current user | Yes |
| GET | `/problems` | List all 10 problems | No |
| GET | `/problem/{id}` | Get problem details | No |
| POST | `/run` | Execute code (playground/run) | Optional |
| POST | `/submit` | Judge against hidden test cases | Optional |
| GET | `/result/{id}` | Get submission result | No |
| GET | `/submissions` | My submission history | Yes |

---

## 🏆 10 Problems

| # | Title | Difficulty |
|---|-------|-----------|
| 1 | Two Sum | Easy |
| 2 | Reverse a String | Easy |
| 3 | Palindrome Check | Easy |
| 4 | Fibonacci Sequence | Easy |
| 5 | Maximum Subarray | Medium |
| 6 | Valid Parentheses | Medium |
| 7 | Binary Search | Medium |
| 8 | Longest Common Subsequence | Hard |
| 9 | Word Ladder | Hard |
| 10 | N-Queens | Hard |

---

## 🐳 Docker Security

Each code execution runs in an isolated container with:
- `--network none` — no internet access
- `--memory 128m` — memory cap
- `--cpu-quota 50000` — 50% CPU limit
- `--pids-limit 50` — process limit
- `--read-only` — read-only filesystem
- `--tmpfs /tmp:size=32m` — temp storage only
- 10-second timeout

---

## 🛠 Tech Stack

- **Frontend**: HTML5 + CSS3 + Vanilla JS, Tailwind-inspired CSS, Monaco Editor
- **Backend**: FastAPI + Uvicorn
- **Database**: SQLite + SQLAlchemy ORM
- **Execution**: Docker containers
- **Auth**: JWT (python-jose) + bcrypt
- **Hosting**: AWS Amplify (frontend) + EC2 (backend)
- **CI/CD**: GitHub → Amplify auto-deploy

---

## 🔑 Environment Variables (Production)

In `backend/routes/auth.py`, change `SECRET_KEY`:
```python
SECRET_KEY = "your-secure-random-secret-key-here"
```

Or better, use an environment variable:
```python
import os
SECRET_KEY = os.getenv("JWT_SECRET", "fallback-dev-key")
```
