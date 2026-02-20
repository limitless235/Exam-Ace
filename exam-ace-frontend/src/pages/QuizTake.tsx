import { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { submitQuiz, type GenerateResponse } from '../api/client';

export default function QuizTake() {
    useParams<{ id: string }>();
    const location = useLocation();
    const navigate = useNavigate();

    const quiz = (location.state as any)?.quiz as GenerateResponse | undefined;
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answers, setAnswers] = useState<(number | null)[]>([]);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!quiz) {
            navigate('/quiz/start', { replace: true });
            return;
        }
        setAnswers(new Array(quiz.questions.length).fill(null));
    }, [quiz, navigate]);

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

    const handleSubmit = async () => {
        if (!allAnswered) return;
        setSubmitting(true);
        setError('');

        // Local quizzes carry correct_index + explanation on each question
        const isLocalQuiz = quiz.quiz_id.startsWith('local-');

        if (isLocalQuiz) {
            const results = quiz.questions.map((q: any, i: number) => {
                const selected = answers[i] as number;
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
            navigate(`/results/${quiz.quiz_id}`, { state: { result: localResult }, replace: true });
            return;
        }

        try {
            const result = await submitQuiz(quiz.quiz_id, answers as number[]);
            navigate(`/results/${quiz.quiz_id}`, { state: { result }, replace: true });
        } catch (err: any) {
            setError(err.message || 'Submission failed');
            setSubmitting(false);
        }
    };

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: '750px' }}>
                {/* Header */}
                <div style={{ marginBottom: 'var(--space-lg)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-sm)' }}>
                        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            {quiz.subject} · <span className={`badge badge-${quiz.difficulty}`}>{quiz.difficulty}</span>
                        </span>
                        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            {answeredCount}/{total} answered
                        </span>
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
                            onClick={handleSubmit}
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
