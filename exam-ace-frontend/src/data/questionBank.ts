/**
 * Frontend question-bank index.
 *
 * Maps every subject name (as shown in QuizStart.tsx) to its bank,
 * and exposes a `sampleFromBank()` helper that picks random questions.
 */

import type { BankQuestion, Difficulty, SubjectBank } from './types';
import { computerScience } from './computerScience';
import { mathematics } from './mathematics';
import { physics, chemistry, biology } from './sciences';
import { history, geography } from './humanities';
import { englishLiterature } from './englishLiterature';
import { economics, psychology } from './socialSciences';
import { generalKnowledge } from './generalKnowledge';
import { dataScience, machineLearning } from './techAI';
import { networking, cybersecurity, softwareEngineering } from './techSystems';

// ─── Full bank keyed by display-name ───────────────────────────
export const questionBank: Record<string, SubjectBank> = {
    'Computer Science': computerScience,
    'Mathematics': mathematics,
    'Physics': physics,
    'Chemistry': chemistry,
    'Biology': biology,
    'History': history,
    'Geography': geography,
    'English Literature': englishLiterature,
    'Economics': economics,
    'Psychology': psychology,
    'General Knowledge': generalKnowledge,
    'Data Science': dataScience,
    'Machine Learning': machineLearning,
    'Networking': networking,
    'Cybersecurity': cybersecurity,
    'Software Engineering': softwareEngineering,
};

// ─── Fisher–Yates shuffle ──────────────────────────────────────
function shuffle<T>(arr: T[]): T[] {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// ─── Public API ────────────────────────────────────────────────

/**
 * Sample `count` random questions from the local bank for the
 * given subject and difficulty.
 *
 * If the subject or difficulty isn't in the bank, returns an empty array.
 */
export function sampleFromBank(
    subject: string,
    difficulty: string,
    count: number,
): BankQuestion[] {
    const bank = questionBank[subject];
    if (!bank) return [];

    const pool = bank[difficulty as Difficulty];
    if (!pool || pool.length === 0) return [];

    return shuffle(pool).slice(0, count);
}

/**
 * Convert a `BankQuestion` into the shape returned by the backend
 * `GenerateResponse.questions` so the quiz-take page can render
 * them identically.
 */
export function bankToApiFormat(
    questions: BankQuestion[],
    subject: string,
    difficulty: string,
) {
    const quizId = `local-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

    return {
        quiz_id: quizId,
        subject,
        difficulty,
        source: 'practice_bank' as const,
        questions: questions.map((q, i) => ({
            id: `${quizId}-q${i}`,
            question: q.question,
            options: q.options,
            correct_index: q.correct_index,
            explanation: q.explanation,
        })),
    };
}
