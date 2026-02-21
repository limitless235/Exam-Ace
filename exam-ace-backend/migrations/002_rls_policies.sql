-- ============================================================
-- ExamAce — Row Level Security Policies
-- Run this in the Supabase SQL Editor AFTER 001_create_tables.sql
-- ============================================================

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;

-- ---- Profiles ----
-- Users can read only their own profile
CREATE POLICY profiles_select_own ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can update only their own profile
CREATE POLICY profiles_update_own ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Insert is handled by the trigger (SECURITY DEFINER), so no insert policy needed for users

-- ---- User Settings ----
CREATE POLICY settings_select_own ON user_settings
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY settings_insert_own ON user_settings
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY settings_update_own ON user_settings
    FOR UPDATE USING (auth.uid() = user_id);

-- ---- Quiz Attempts ----
CREATE POLICY quiz_select_own ON quiz_attempts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY quiz_insert_own ON quiz_attempts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY quiz_update_own ON quiz_attempts
    FOR UPDATE USING (auth.uid() = user_id);

-- No DELETE policy — quiz history is immutable
-- No anonymous access — all policies require auth.uid()
