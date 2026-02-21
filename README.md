# Exam Ace

An AI-powered exam preparation platform that generates quizzes tailored to your subject and difficulty level, tracks your performance over time, and helps you study smarter.

I built this because I wanted something that goes beyond static flashcards and last minute revisions. It is a tool that actually adapts to what you're studying and gives you immediate feedback with explanations.

## Screenshots

![Screenshot 1](<images/WhatsApp Image 2026-02-21 at 11.15.27.jpeg>)
*Quiz UI*

![Screenshot 2](<images/WhatsApp Image 2026-02-21 at 11.15.44.jpeg>)
*Score page after completion of quiz along with explanations to questions*

![Screenshot 3](<images/WhatsApp Image 2026-02-21 at 11.16.11.jpeg>)
*Performance Page*

![Screenshot 4](<images/WhatsApp Image 2026-02-21 at 11.16.30.jpeg>)
*Settings Page*

![Screenshot 5](<images/WhatsApp Image 2026-02-21 at 11.16.51.jpeg>)
*Dashboard Page*

![Screenshot 6](<images/WhatsApp Image 2026-02-21 at 11.17.16.jpeg>)
*Quiz Configuration Page*

![Screenshot 7](<images/WhatsApp Image 2026-02-21 at 11.17.31.jpeg>)
*Authentication Page*

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
