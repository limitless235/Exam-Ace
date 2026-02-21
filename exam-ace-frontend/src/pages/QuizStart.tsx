import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSettings, generateQuiz, type UserSettings } from '../api/client';
import { sampleFromBank, bankToApiFormat } from '../data/questionBank';

const SUBJECTS = [
    'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology',
    'History', 'Geography', 'English Literature', 'Economics', 'Psychology',
    'General Knowledge', 'Data Science', 'Machine Learning', 'Networking',
    'Cybersecurity', 'Software Engineering',
];

export default function QuizStart() {
    const navigate = useNavigate();
    const [, setSettings] = useState<UserSettings | null>(null);
    const [subject, setSubject] = useState('Computer Science');
    const [difficulty, setDifficulty] = useState('beginner');
    const [count, setCount] = useState(10);
    const [timeLimit, setTimeLimit] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [settingsLoading, setSettingsLoading] = useState(true);

    useEffect(() => {
        getSettings()
            .then((s) => {
                setSettings(s);
                setSubject(s.subject);
                setDifficulty(s.difficulty);
                setCount(s.question_count);
                setTimeLimit(s.time_limit);
            })
            .catch(console.error)
            .finally(() => setSettingsLoading(false));
    }, []);

    const handleGenerate = async () => {
        setError('');
        setLoading(true);
        try {
            // Try the backend API first
            const res = await generateQuiz(subject, difficulty, count);

            // If the backend returned practice_bank questions (LLM offline),
            // use the richer frontend bank instead (960 questions, all 16 subjects)
            if (res.source === 'practice_bank') {
                const localQuestions = sampleFromBank(subject, difficulty, count);
                if (localQuestions.length > 0) {
                    const localQuiz = bankToApiFormat(localQuestions, subject, difficulty);
                    navigate(`/quiz/${localQuiz.quiz_id}`, { state: { quiz: localQuiz, timeLimit } });
                    return;
                }
            }

            navigate(`/quiz/${res.quiz_id}`, { state: { quiz: res, timeLimit } });
        } catch {
            // Backend entirely unavailable — fall back to local question bank
            const questions = sampleFromBank(subject, difficulty, count);
            if (questions.length === 0) {
                setError('No questions available for this subject/difficulty.');
            } else {
                const localQuiz = bankToApiFormat(questions, subject, difficulty);
                navigate(`/quiz/${localQuiz.quiz_id}`, { state: { quiz: localQuiz, timeLimit } });
            }
        } finally {
            setLoading(false);
        }
    };

    if (settingsLoading) {
        return (
            <div className="page">
                <div className="container loading-state">
                    <div className="spinner" />
                    <p>Loading your preferences…</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: '600px' }}>
                <div className="page-header" style={{ textAlign: 'center' }}>
                    <h1>Configure Your Quiz</h1>
                    <p>Adjust the settings below, then hit generate.</p>
                </div>

                {error && <div className="error-message">{error}</div>}

                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
                    {/* Subject */}
                    <div className="form-group">
                        <label className="form-label" htmlFor="subject">Subject</label>
                        <select
                            id="subject"
                            className="form-select"
                            value={subject}
                            onChange={(e) => setSubject(e.target.value)}
                        >
                            {SUBJECTS.map((s) => (
                                <option key={s} value={s}>{s}</option>
                            ))}
                        </select>
                    </div>

                    {/* Difficulty */}
                    <div className="form-group">
                        <label className="form-label">Difficulty</label>
                        <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
                            {['beginner', 'intermediate', 'advanced'].map((d) => (
                                <button
                                    key={d}
                                    className={`btn ${difficulty === d ? 'btn-primary' : 'btn-secondary'}`}
                                    onClick={() => setDifficulty(d)}
                                    style={{ flex: 1, textTransform: 'capitalize' }}
                                    type="button"
                                >
                                    {d}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Question Count */}
                    <div className="form-group">
                        <label className="form-label" htmlFor="count">
                            Number of Questions: <strong style={{ color: 'var(--text-primary)' }}>{count}</strong>
                        </label>
                        <input
                            id="count"
                            type="range"
                            min={3}
                            max={30}
                            value={count}
                            onChange={(e) => setCount(Number(e.target.value))}
                            style={{ width: '100%', accentColor: 'var(--accent-primary)' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            <span>3</span><span>30</span>
                        </div>
                    </div>

                    {/* Generate Button */}
                    <button
                        className="btn btn-primary btn-lg"
                        onClick={handleGenerate}
                        disabled={loading}
                        style={{ marginTop: 'var(--space-md)' }}
                    >
                        {loading ? (
                            <>
                                <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} />
                                Generating with AI…
                            </>
                        ) : (
                            'Generate Quiz'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
