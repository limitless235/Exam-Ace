import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuizHistory, getSettings, type QuizHistoryItem, type UserSettings } from '../api/client';
import { useAuth } from '../hooks/useAuth';

export default function Dashboard() {
    const { user } = useAuth();
    const [history, setHistory] = useState<QuizHistoryItem[]>([]);
    const [settings, setSettings] = useState<UserSettings | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            getQuizHistory().catch(() => [] as QuizHistoryItem[]),
            getSettings().catch(() => null),
        ])
            .then(([h, s]) => { setHistory(h); setSettings(s); })
            .finally(() => setLoading(false));
    }, []);

    const displayName = user?.user_metadata?.display_name || user?.email?.split('@')[0] || 'Student';
    const recentQuizzes = history.slice(0, 5);
    const totalQuizzes = history.length;
    const avgScore = history.filter(h => h.score !== null).length > 0
        ? (history.filter(h => h.score !== null).reduce((a, b) => a + (b.score ?? 0), 0) / history.filter(h => h.score !== null).length).toFixed(1)
        : '—';

    if (loading) {
        return (
            <div className="page">
                <div className="container loading-state">
                    <div className="spinner" />
                    <p>Loading your dashboard…</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page">
            <div className="container">
                <div className="page-header">
                    <h1>Welcome back, {displayName}</h1>
                    <p>Ready to ace your next exam? Let's get studying.</p>
                </div>

                {/* Quick Stats */}
                <div className="grid-3" style={{ marginBottom: 'var(--space-2xl)' }}>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{totalQuizzes}</div>
                        <div className="stat-label">Quizzes Taken</div>
                    </div>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{avgScore}%</div>
                        <div className="stat-label">Average Score</div>
                    </div>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{settings?.subject || '—'}</div>
                        <div className="stat-label">Current Subject</div>
                    </div>
                </div>

                {/* Start Quiz CTA */}
                <div className="glass-card" style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)', padding: 'var(--space-2xl)' }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: 'var(--space-sm)' }}>Start a New Quiz</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-lg)' }}>
                        Generate an AI-powered quiz tailored to your settings.
                    </p>
                    <Link to="/quiz/start" className="btn btn-primary btn-lg">
                        Generate Quiz
                    </Link>
                </div>

                {/* Recent Activity */}
                <div className="glass-card">
                    <h3 style={{ marginBottom: 'var(--space-lg)', fontWeight: 700 }}>Recent Activity</h3>
                    {recentQuizzes.length === 0 ? (
                        <div className="empty-state">
                            <div className="icon"></div>
                            <p>No quizzes yet. Start your first one!</p>
                        </div>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                            {recentQuizzes.map((q) => (
                                <Link
                                    key={q.id}
                                    to={q.score !== null ? `/results/${q.id}` : `/quiz/${q.id}`}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'space-between',
                                        padding: 'var(--space-md) var(--space-lg)',
                                        background: 'var(--bg-glass)',
                                        borderRadius: 'var(--radius-md)',
                                        border: '1px solid var(--border-glass)',
                                        transition: 'all 0.2s ease',
                                        textDecoration: 'none',
                                        color: 'var(--text-primary)',
                                    }}
                                >
                                    <div>
                                        <strong>{q.subject}</strong>
                                        <span className={`badge badge-${q.difficulty}`} style={{ marginLeft: '0.5rem' }}>
                                            {q.difficulty}
                                        </span>
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                        {q.score !== null && (
                                            <span style={{ fontWeight: 700, color: q.score >= 70 ? 'var(--success)' : q.score >= 40 ? 'var(--warning)' : 'var(--error)' }}>
                                                {q.score}%
                                            </span>
                                        )}
                                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                            {q.created_at ? new Date(q.created_at).toLocaleDateString() : ''}
                                        </span>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
