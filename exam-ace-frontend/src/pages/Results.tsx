import { useLocation, Link } from 'react-router-dom';
import type { SubmitResponse } from '../api/client';

export default function Results() {
    const location = useLocation();
    const result = (location.state as any)?.result as SubmitResponse | undefined;

    if (!result) {
        return (
            <div className="page">
                <div className="container" style={{ textAlign: 'center' }}>
                    <div className="empty-state">
                        <div className="icon"></div>
                        <p>No results to display.</p>
                        <Link to="/dashboard" className="btn btn-primary" style={{ marginTop: '1rem' }}>Back to Dashboard</Link>
                    </div>
                </div>
            </div>
        );
    }

    const scoreColor = result.score >= 70 ? 'var(--success)' : result.score >= 40 ? 'var(--warning)' : 'var(--error)';

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: '750px' }}>
                {/* Score Circle */}
                <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)', animation: 'slideUp 0.4s ease' }}>
                    <div className="score-circle">
                        <span className="score-value">{result.score}%</span>
                        <span className="score-label">Score</span>
                    </div>
                    <h1 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: 'var(--space-xs)' }}>
                        {result.score >= 80 ? 'Excellent!' : result.score >= 60 ? 'Good Job!' : result.score >= 40 ? 'Keep Practicing' : 'Don\'t Give Up!'}
                    </h1>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        You got <strong style={{ color: scoreColor }}>{result.correct}</strong> out of <strong>{result.total}</strong> correct
                    </p>
                </div>

                {/* Question Review */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
                    {result.results.map((q, i) => (
                        <div
                            key={i}
                            className="glass-card"
                            style={{ animation: `slideUp ${0.3 + i * 0.05}s ease` }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', marginBottom: 'var(--space-md)' }}>
                                <span style={{
                                    width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    background: q.is_correct ? 'var(--success-bg)' : 'var(--error-bg)',
                                    color: q.is_correct ? 'var(--success)' : 'var(--error)',
                                    fontSize: '0.8rem', fontWeight: 700,
                                }}>
                                    {q.is_correct ? '✓' : '✗'}
                                </span>
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Question {i + 1}</span>
                            </div>

                            <h3 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: 'var(--space-md)', lineHeight: 1.5 }}>
                                {q.question}
                            </h3>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xs)' }}>
                                {q.options.map((opt, oi) => {
                                    let className = 'quiz-option';
                                    if (oi === q.correct_index) className += ' correct';
                                    else if (oi === q.selected_index && !q.is_correct) className += ' incorrect';
                                    return (
                                        <div key={oi} className={className} style={{ cursor: 'default' }}>
                                            <span className="option-letter">{String.fromCharCode(65 + oi)}</span>
                                            <span>{opt}</span>
                                            {oi === q.correct_index && (
                                                <span style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--success)' }}>✓ Correct</span>
                                            )}
                                            {oi === q.selected_index && oi !== q.correct_index && (
                                                <span style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--error)' }}>Your answer</span>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>

                            <div className="explanation-box">
                                {q.explanation}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-md)', marginTop: 'var(--space-2xl)' }}>
                    <Link to="/quiz/start" className="btn btn-primary btn-lg">New Quiz</Link>
                    <Link to="/dashboard" className="btn btn-secondary btn-lg">Dashboard</Link>
                </div>
            </div>
        </div>
    );
}
