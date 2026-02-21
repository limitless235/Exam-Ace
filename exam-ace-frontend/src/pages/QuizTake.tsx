import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { submitQuiz, recordQuizAttempt, type GenerateResponse } from '../api/client';

export default function QuizTake() {
    useParams<{ id: string }>();
    const location = useLocation();
    const navigate = useNavigate();

    const quiz = (location.state as any)?.quiz as GenerateResponse | undefined;
    const timeLimit = (location.state as any)?.timeLimit as number | null | undefined;
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answers, setAnswers] = useState<(number | null)[]>([]);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');

    // Timer state (in seconds)
    const [timeRemaining, setTimeRemaining] = useState<number | null>(
        timeLimit ? timeLimit * 60 : null
    );
    const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
    const hasAutoSubmitted = useRef(false);

    useEffect(() => {
        if (!quiz) {
            navigate('/quiz/start', { replace: true });
            return;
        }
        setAnswers(new Array(quiz.questions.length).fill(null));
    }, [quiz, navigate]);

    // Countdown timer
    useEffect(() => {
        if (timeRemaining === null || timeRemaining <= 0) return;

        timerRef.current = setInterval(() => {
            setTimeRemaining((prev) => {
                if (prev === null) return null;
                if (prev <= 1) {
                    if (timerRef.current) clearInterval(timerRef.current);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, [timeRemaining === null]); // only re-run if timer existence changes

    // Auto-submit when timer hits 0
    const handleSubmit = useCallback(async (forceSubmit = false) => {
        if (!quiz) return;
        const finalAnswers = forceSubmit ? answers.map(a => a ?? 0) : answers;
        const allAnswered = finalAnswers.every(a => a !== null);
        if (!allAnswered && !forceSubmit) return;

        setSubmitting(true);
        setError('');

        const isLocalQuiz = quiz.quiz_id.startsWith('local-');

        if (isLocalQuiz) {
            const results = quiz.questions.map((q: any, i: number) => {
                const selected = finalAnswers[i] as number;
                return {
                    question: q.question,
                    options: q.options,
                    selected_index: selected,
                    correct_index: q.correct_index,
                    is_correct: selected === q.correct_index,
                    explanation: q.explanation ?? '',
                };
            });
            const correctCount = results.filter((r) => r.is_correct).length;
            const localResult = {
                quiz_id: quiz.quiz_id,
                score: Math.round((correctCount / results.length) * 100),
                total: results.length,
                correct: correctCount,
                results,
            };
            recordQuizAttempt(quiz.subject, quiz.difficulty, localResult.score, localResult.total, localResult.correct)
                .catch(() => { });

            navigate(`/results/${quiz.quiz_id}`, { state: { result: localResult }, replace: true });
            return;
        }

        try {
            const result = await submitQuiz(quiz.quiz_id, finalAnswers as number[]);
            navigate(`/results/${quiz.quiz_id}`, { state: { result }, replace: true });
        } catch (err: any) {
            setError(err.message || 'Submission failed');
            setSubmitting(false);
        }
    }, [quiz, answers, navigate]);

    // Watch for timer expiry
    useEffect(() => {
        if (timeRemaining === 0 && !hasAutoSubmitted.current && quiz) {
            hasAutoSubmitted.current = true;
            handleSubmit(true);
        }
    }, [timeRemaining, quiz, handleSubmit]);

    if (!quiz) return null;

    const question = quiz.questions[currentIndex];
    const total = quiz.questions.length;
    const answeredCount = answers.filter((a) => a !== null).length;
    const allAnswered = answeredCount === total;
    const progress = ((currentIndex + 1) / total) * 100;

    const selectOption = (optionIndex: number) => {
        const next = [...answers];
        next[currentIndex] = optionIndex;
        setAnswers(next);
    };

    // Format seconds as MM:SS
    const formatTime = (seconds: number) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const isTimeLow = timeRemaining !== null && timeRemaining <= 60;

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: '750px' }}>
                {/* Header */}
                <div style={{ marginBottom: 'var(--space-lg)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-sm)' }}>
                        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            {quiz.subject} · <span className={`badge badge-${quiz.difficulty}`}>{quiz.difficulty}</span>
                        </span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            {timeRemaining !== null && (
                                <span style={{
                                    fontSize: '1rem',
                                    fontWeight: 700,
                                    fontFamily: 'monospace',
                                    color: isTimeLow ? 'var(--error)' : 'var(--accent-primary)',
                                    background: isTimeLow ? 'rgba(239,68,68,0.1)' : 'var(--bg-glass)',
                                    padding: '0.25rem 0.75rem',
                                    borderRadius: 'var(--radius-md)',
                                    border: `1px solid ${isTimeLow ? 'rgba(239,68,68,0.3)' : 'var(--border-glass)'}`,
                                    animation: isTimeLow ? 'pulse 1s ease-in-out infinite' : 'none',
                                }}>
                                    {formatTime(timeRemaining)}
                                </span>
                            )}
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                {answeredCount}/{total} answered
                            </span>
                        </div>
                    </div>
                    <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${progress}%` }} />
                    </div>
                </div>

                {error && <div className="error-message">{error}</div>}

                {/* Question Card */}
                <div className="glass-card" style={{ animation: 'slideUp 0.3s ease' }}>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 'var(--space-sm)' }}>
                        Question {currentIndex + 1} of {total}
                    </div>
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: 'var(--space-xl)', lineHeight: 1.5 }}>
                        {question.question}
                    </h2>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                        {question.options.map((opt, i) => (
                            <button
                                key={i}
                                className={`quiz-option ${answers[currentIndex] === i ? 'selected' : ''}`}
                                onClick={() => selectOption(i)}
                                type="button"
                            >
                                <span className="option-letter">
                                    {String.fromCharCode(65 + i)}
                                </span>
                                <span>{opt}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Navigation */}
                <div className="quiz-nav">
                    <button
                        className="btn btn-secondary"
                        onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
                        disabled={currentIndex === 0}
                    >
                        ← Previous
                    </button>

                    <div style={{ display: 'flex', gap: 'var(--space-xs)', flexWrap: 'wrap', justifyContent: 'center' }}>
                        {quiz.questions.map((_, i) => (
                            <button
                                key={i}
                                onClick={() => setCurrentIndex(i)}
                                style={{
                                    width: 32,
                                    height: 32,
                                    borderRadius: '50%',
                                    border: i === currentIndex ? '2px solid var(--accent-primary)' : '1px solid var(--border-glass)',
                                    background: answers[i] !== null
                                        ? 'var(--accent-primary)'
                                        : 'var(--bg-glass)',
                                    color: answers[i] !== null ? 'white' : 'var(--text-secondary)',
                                    cursor: 'pointer',
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    fontFamily: 'Inter, sans-serif',
                                    transition: 'all 0.15s ease',
                                }}
                            >
                                {i + 1}
                            </button>
                        ))}
                    </div>

                    {currentIndex < total - 1 ? (
                        <button
                            className="btn btn-secondary"
                            onClick={() => setCurrentIndex(currentIndex + 1)}
                        >
                            Next →
                        </button>
                    ) : (
                        <button
                            className="btn btn-primary"
                            onClick={() => handleSubmit(false)}
                            disabled={!allAnswered || submitting}
                        >
                            {submitting ? 'Submitting…' : 'Submit Quiz'}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
