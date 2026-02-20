-- ============================================================
-- ExamAce — Core Tables
-- Run this in the Supabase SQL Editor
-- ============================================================

-- 1. Profiles
CREATE TABLE IF NOT EXISTS profiles (
    id          UUID PRIMARY KEY,
    email       TEXT UNIQUE NOT NULL,
    display_name TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Auto-create a profile when a new Supabase auth user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO public.profiles (id, email, display_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data ->> 'display_name', split_part(NEW.email, '@', 1))
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


-- 2. User Settings
CREATE TABLE IF NOT EXISTS user_settings (
    user_id         UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    subject         TEXT NOT NULL DEFAULT 'General Knowledge',
    difficulty      TEXT NOT NULL DEFAULT 'beginner'
                    CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    question_count  INT NOT NULL DEFAULT 10
                    CHECK (question_count BETWEEN 3 AND 30),
    time_limit      INT DEFAULT NULL
                    CHECK (time_limit IS NULL OR time_limit BETWEEN 1 AND 120),
    auto_submit     BOOLEAN NOT NULL DEFAULT FALSE,
    show_explanations BOOLEAN NOT NULL DEFAULT TRUE
);


-- 3. Quiz Attempts
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    subject     TEXT NOT NULL,
    difficulty  TEXT NOT NULL
                CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    questions   JSONB NOT NULL,
    answers     JSONB,
    score       FLOAT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Index for fast history queries
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_created
    ON quiz_attempts (user_id, created_at DESC);
