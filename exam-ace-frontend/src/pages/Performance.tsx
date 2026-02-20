import { useEffect, useState } from 'react';
import { getPerformance, type PerformanceData } from '../api/client';

export default function Performance() {
    const [data, setData] = useState<PerformanceData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        getPerformance()
            .then(setData)
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="page">
                <div className="container loading-state">
                    <div className="spinner" />
                    <p>Loading performance data…</p>
                </div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="page">
                <div className="container">
                    <div className="error-message">{error || 'Failed to load performance data.'}</div>
                </div>
            </div>
        );
    }

    const { overall, by_subject, by_difficulty, recent } = data;

    return (
        <div className="page">
            <div className="container">
                <div className="page-header">
                    <h1>Performance</h1>
                    <p>Track your progress and identify areas for improvement.</p>
                </div>

                {/* Overall Stats */}
                <div className="grid-4" style={{ marginBottom: 'var(--space-2xl)' }}>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{overall.total_quizzes}</div>
                        <div className="stat-label">Total Quizzes</div>
                    </div>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{overall.avg_score.toFixed(1)}%</div>
                        <div className="stat-label">Average Score</div>
                    </div>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{overall.best_score.toFixed(0)}%</div>
                        <div className="stat-label">Best Score</div>
                    </div>
                    <div className="glass-card stat-card">
                        <div className="stat-value">{overall.worst_score.toFixed(0)}%</div>
                        <div className="stat-label">Worst Score</div>
                    </div>
                </div>

                <div className="grid-2" style={{ marginBottom: 'var(--space-2xl)' }}>
                    {/* By Subject */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: 'var(--space-lg)', fontWeight: 700 }}>By Subject</h3>
                        {by_subject.length === 0 ? (
                            <p style={{ color: 'var(--text-muted)' }}>No data yet</p>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
                                {by_subject.map((s) => (
                                    <div key={s.subject}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-xs)' }}>
                                            <span style={{ fontWeight: 500, fontSize: '0.9rem' }}>{s.subject}</span>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                                {s.avg_score}% avg · {s.attempts} quiz{s.attempts !== 1 ? 'zes' : ''}
                                            </span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-fill"
                                                style={{ width: `${s.avg_score}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* By Difficulty */}
                    <div className="glass-card">
                        <h3 style={{ marginBottom: 'var(--space-lg)', fontWeight: 700 }}>By Difficulty</h3>
                        {by_difficulty.length === 0 ? (
                            <p style={{ color: 'var(--text-muted)' }}>No data yet</p>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
                                {by_difficulty.map((d) => (
                                    <div key={d.difficulty}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-xs)' }}>
                                            <span className={`badge badge-${d.difficulty}`} style={{ textTransform: 'capitalize' }}>
                                                {d.difficulty}
                                            </span>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                                {d.avg_score}% avg · {d.attempts} quiz{d.attempts !== 1 ? 'zes' : ''}
                                            </span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-fill"
                                                style={{ width: `${d.avg_score}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* Recent Trend */}
                <div className="glass-card">
                    <h3 style={{ marginBottom: 'var(--space-lg)', fontWeight: 700 }}>Recent Quizzes</h3>
                    {recent.length === 0 ? (
                        <div className="empty-state">
                            <div className="icon"></div>
                            <p>Complete some quizzes to see your trend!</p>
                        </div>
                    ) : (
                        <div style={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border-glass)' }}>
                                        <th style={{ textAlign: 'left', padding: '0.75rem', fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Subject</th>
                                        <th style={{ textAlign: 'left', padding: '0.75rem', fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Difficulty</th>
                                        <th style={{ textAlign: 'right', padding: '0.75rem', fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Score</th>
                                        <th style={{ textAlign: 'right', padding: '0.75rem', fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {recent.map((r, i) => (
                                        <tr key={i} style={{ borderBottom: '1px solid var(--border-glass)' }}>
                                            <td style={{ padding: '0.75rem', fontWeight: 500 }}>{r.subject}</td>
                                            <td style={{ padding: '0.75rem' }}>
                                                <span className={`badge badge-${r.difficulty}`}>{r.difficulty}</span>
                                            </td>
                                            <td style={{
                                                padding: '0.75rem',
                                                textAlign: 'right',
                                                fontWeight: 700,
                                                color: r.score >= 70 ? 'var(--success)' : r.score >= 40 ? 'var(--warning)' : 'var(--error)',
                                            }}>
                                                {r.score}%
                                            </td>
                                            <td style={{ padding: '0.75rem', textAlign: 'right', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                                {r.created_at ? new Date(r.created_at).toLocaleDateString() : '—'}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
