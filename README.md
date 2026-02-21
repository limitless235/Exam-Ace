# Exam Ace

An AI-powered exam preparation platform that generates quizzes tailored to your subject and difficulty level, tracks your performance over time, and helps you study smarter.

I built this because I wanted something that goes beyond static flashcards — a tool that actually adapts to what you're studying and gives you immediate feedback with explanations.

## What it does

- **AI-generated quizzes** — Pick a subject and difficulty, and the app generates unique questions using a local LLM (Phi-3 mini via LM Studio). If the LLM isn't available, it falls back to a built-in bank of 960 questions across 16 subjects.
- **Instant scoring & explanations** — After submitting a quiz, you get your score along with explanations for every question, so you actually learn from mistakes.
- **Performance tracking** — Every quiz result is logged. The performance dashboard breaks down your scores by subject, difficulty, and shows your recent trend.
- **Configurable settings** — Choose your preferred subject, difficulty level, number of questions, and time limits.
- **Google OAuth** — Sign in with Google through Supabase auth. No passwords to remember.

## Tech stack

**Frontend**
- React 19 + TypeScript
- Vite for builds
- React Router for navigation
- Supabase JS for auth
- Vanilla CSS with glassmorphism design

**Backend**
- FastAPI (Python)
- asyncpg for Postgres queries
- Redis for rate limiting
- python-jose for JWT verification
- Supabase for auth and database (Postgres)

**Infrastructure**
- Frontend hosted on Vercel
- Backend hosted on Render
- Database on Supabase (Postgres)
- Redis on Upstash
- LM Studio + ngrok for local LLM serving

## Project structure

```
ExamPrepApp/
├── exam-ace-frontend/       # React + Vite app
│   ├── src/
│   │   ├── api/             # API client functions
│   │   ├── components/      # Shared components (Navbar, ProtectedRoute)
│   │   ├── data/            # Local question bank (960 questions)
│   │   ├── hooks/           # useAuth hook
│   │   └── pages/           # Dashboard, Quiz, Results, Performance, Settings, Login
│   └── vercel.json          # SPA routing config
│
├── exam-ace-backend/        # FastAPI app
│   ├── app/
│   │   ├── auth/            # JWT middleware & dependencies
│   │   ├── core/            # Config, database pool, rate limiter
│   │   ├── quiz/            # Quiz generation, LLM gateway, question bank
│   │   ├── analytics/       # Performance aggregation endpoint
│   │   ├── settings/        # User settings CRUD
│   │   └── users/           # User profile endpoint
│   └── migrations/          # SQL for tables, triggers, RLS policies
│
└── README.md
```

## Running locally

### Prerequisites
- Node.js 18+
- Python 3.11
- A Supabase project (free tier works)
- Redis (or Upstash free tier)
- LM Studio (optional, for AI question generation)

### Frontend

```bash
cd exam-ace-frontend
npm install

# Create .env
echo "VITE_SUPABASE_URL=https://your-project.supabase.co" > .env
echo "VITE_SUPABASE_ANON_KEY=your-anon-key" >> .env
echo "VITE_API_BASE=http://localhost:8000" >> .env

npm run dev
```

### Backend

```bash
cd exam-ace-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
cat > .env <<EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
REDIS_URL=redis://localhost:6379
LLM_PROVIDER=local
LLM_BASE_URL=http://localhost:1234/v1
CORS_ORIGINS=http://localhost:5173
EOF

uvicorn app.main:app --reload
```

### Database setup

Run these in the Supabase SQL Editor:
1. `migrations/001_create_tables.sql` — Creates profiles, user_settings, quiz_attempts tables + auto-profile trigger
2. `migrations/002_rls_policies.sql` — Row Level Security policies

## How quiz generation works

There's a three-tier fallback system so quizzes always work, even offline:

1. **LLM generation** — If LM Studio is running (locally or via ngrok tunnel), the backend sends a prompt and gets back unique, AI-generated questions.
2. **Backend question bank** — If the LLM is unreachable, the backend picks from its own curated question bank.
3. **Frontend question bank** — If the entire backend is down (Render cold start, network issues), the frontend generates quizzes from a local bank of 960 questions across 16 subjects.

Quiz results are always saved to the database for performance tracking, regardless of which tier generated the questions.

## Using LM Studio in production

Since the backend runs on Render and LM Studio runs on your laptop, you need a tunnel:

```bash
# 1. Start LM Studio with a model loaded
# 2. Expose it with ngrok
ngrok http 1234

# 3. Copy the public URL and set it on Render:
#    LLM_BASE_URL = https://your-ngrok-url.ngrok-free.dev/v1
```

When ngrok isn't running, the app gracefully falls back to the question banks.

## Environment variables

### Frontend (Vercel)
| Variable | Description |
|---|---|
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon/public key |
| `VITE_API_BASE` | Backend URL (Render) |

### Backend (Render)
| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_JWT_SECRET` | JWT secret from Supabase |
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Redis connection URL |
| `LLM_PROVIDER` | `local` for LM Studio |
| `LLM_BASE_URL` | LM Studio URL (direct or via ngrok) |
| `LLM_HEALTH_TIMEOUT` | Timeout in seconds for LLM health check |
| `CORS_ORIGINS` | Frontend URL (Vercel) |

## License

MIT
