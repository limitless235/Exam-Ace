/**
 * Typed API client — all calls go through here.
 * Token is pulled from Supabase session automatically.
 */
import { supabase } from './supabase';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

async function getToken(): Promise<string> {
    const { data } = await supabase.auth.getSession();
    const token = data.session?.access_token;
    if (!token) throw new Error('Not authenticated');
    return token;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = await getToken();
    const res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            ...options.headers,
        },
    });

    if (!res.ok) {
        const body = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(body.detail || `API error ${res.status}`);
    }

    return res.json();
}

// --- Quiz ---
export interface QuizQuestionPublic {
    index: number;
    question: string;
    options: string[];
}

export interface GenerateResponse {
    quiz_id: string;
    questions: QuizQuestionPublic[];
    subject: string;
    difficulty: string;
    source: 'ai' | 'practice_bank';
}

export interface QuestionResult {
    question: string;
    options: string[];
    selected_index: number;
    correct_index: number;
    is_correct: boolean;
    explanation: string;
}

export interface SubmitResponse {
    quiz_id: string;
    score: number;
    total: number;
    correct: number;
    results: QuestionResult[];
}

export interface QuizHistoryItem {
    id: string;
    subject: string;
    difficulty: string;
    score: number | null;
    created_at: string | null;
}

export function generateQuiz(subject: string, difficulty: string, count: number) {
    return request<GenerateResponse>('/quiz/generate', {
        method: 'POST',
        body: JSON.stringify({ subject, difficulty, count }),
    });
}

export function submitQuiz(quiz_id: string, answers: number[]) {
    return request<SubmitResponse>('/quiz/submit', {
        method: 'POST',
        body: JSON.stringify({ quiz_id, answers }),
    });
}

export function getQuizHistory() {
    return request<QuizHistoryItem[]>('/quiz/history');
}

export function recordQuizAttempt(subject: string, difficulty: string, score: number, total: number, correct: number) {
    return request<{ status: string; id: string }>('/quiz/record', {
        method: 'POST',
        body: JSON.stringify({ subject, difficulty, score, total, correct }),
    });
}

// --- Settings ---
export interface UserSettings {
    subject: string;
    difficulty: string;
    question_count: number;
    time_limit: number | null;
    auto_submit: boolean;
    show_explanations: boolean;
}

export function getSettings() {
    return request<UserSettings>('/settings');
}

export function updateSettings(settings: UserSettings) {
    return request<UserSettings>('/settings', {
        method: 'PUT',
        body: JSON.stringify(settings),
    });
}

// --- User ---
export interface UserProfile {
    id: string;
    email: string;
    display_name: string | null;
    created_at: string | null;
}

export function getMe() {
    return request<UserProfile>('/users/me');
}

// --- Analytics ---
export interface PerformanceData {
    overall: {
        total_quizzes: number;
        avg_score: number;
        best_score: number;
        worst_score: number;
    };
    by_subject: { subject: string; attempts: number; avg_score: number }[];
    by_difficulty: { difficulty: string; attempts: number; avg_score: number }[];
    recent: { subject: string; difficulty: string; score: number; created_at: string }[];
}

export function getPerformance() {
    return request<PerformanceData>('/analytics/performance');
}
