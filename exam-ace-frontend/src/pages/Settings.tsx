import { useEffect, useState } from 'react';
import { getSettings, updateSettings, type UserSettings } from '../api/client';

export default function Settings() {
    const [settings, setSettings] = useState<UserSettings | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        getSettings()
            .then(setSettings)
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    }, []);

    const handleSave = async () => {
        if (!settings) return;
        setSaving(true);
        setError('');
        setSaved(false);
        try {
            const updated = await updateSettings(settings);
            setSettings(updated);
            setSaved(true);
            setTimeout(() => setSaved(false), 3000);
        } catch (err: any) {
            setError(err.message || 'Failed to save settings');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="page">
                <div className="container loading-state">
                    <div className="spinner" />
                    <p>Loading settings…</p>
                </div>
            </div>
        );
    }

    if (!settings) return null;

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: '600px' }}>
                <div className="page-header">
                    <h1>⚙️ Settings</h1>
                    <p>Configure your default quiz preferences. Changes are saved server-side.</p>
                </div>

                {error && <div className="error-message">{error}</div>}
                {saved && (
                    <div style={{
                        padding: 'var(--space-sm) var(--space-md)',
                        background: 'var(--success-bg)',
                        border: '1px solid rgba(16,185,129,0.3)',
                        borderRadius: 'var(--radius-md)',
                        color: 'var(--success)',
                        fontSize: '0.85rem',
                        marginBottom: 'var(--space-md)',
                    }}>
                        Settings saved successfully!
                    </div>
                )}

                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
                    {/* Default Subject */}
                    <div className="form-group">
                        <label className="form-label" htmlFor="settings-subject">Default Subject</label>
                        <input
                            id="settings-subject"
                            className="form-input"
                            type="text"
                            value={settings.subject}
                            onChange={(e) => setSettings({ ...settings, subject: e.target.value })}
                        />
                    </div>

                    {/* Default Difficulty */}
                    <div className="form-group">
                        <label className="form-label">Default Difficulty</label>
                        <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
                            {['beginner', 'intermediate', 'advanced'].map((d) => (
                                <button
                                    key={d}
                                    className={`btn ${settings.difficulty === d ? 'btn-primary' : 'btn-secondary'}`}
                                    onClick={() => setSettings({ ...settings, difficulty: d })}
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
                        <label className="form-label" htmlFor="settings-count">
                            Default Question Count: <strong style={{ color: 'var(--text-primary)' }}>{settings.question_count}</strong>
                        </label>
                        <input
                            id="settings-count"
                            type="range"
                            min={3}
                            max={30}
                            value={settings.question_count}
                            onChange={(e) => setSettings({ ...settings, question_count: Number(e.target.value) })}
                            style={{ width: '100%', accentColor: 'var(--accent-primary)' }}
                        />
                    </div>

                    {/* Time Limit */}
                    <div className="form-group">
                        <label className="form-label" htmlFor="settings-time">Time Limit (minutes, blank = no limit)</label>
                        <input
                            id="settings-time"
                            className="form-input"
                            type="number"
                            min={1}
                            max={120}
                            value={settings.time_limit ?? ''}
                            onChange={(e) =>
                                setSettings({ ...settings, time_limit: e.target.value ? Number(e.target.value) : null })
                            }
                            placeholder="No limit"
                        />
                    </div>

                    {/* Auto Submit */}
                    <div className="toggle-wrapper">
                        <div>
                            <div style={{ fontWeight: 500 }}>Auto-submit on time up</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Automatically submit when the timer runs out</div>
                        </div>
                        <label className="toggle">
                            <input
                                type="checkbox"
                                checked={settings.auto_submit}
                                onChange={(e) => setSettings({ ...settings, auto_submit: e.target.checked })}
                            />
                            <span className="toggle-slider" />
                        </label>
                    </div>

                    {/* Show Explanations */}
                    <div className="toggle-wrapper">
                        <div>
                            <div style={{ fontWeight: 500 }}>Show explanations</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Display answer explanations on the results page</div>
                        </div>
                        <label className="toggle">
                            <input
                                type="checkbox"
                                checked={settings.show_explanations}
                                onChange={(e) => setSettings({ ...settings, show_explanations: e.target.checked })}
                            />
                            <span className="toggle-slider" />
                        </label>
                    </div>

                    {/* Save Button */}
                    <button
                        className="btn btn-primary btn-lg"
                        onClick={handleSave}
                        disabled={saving}
                    >
                        {saving ? 'Saving…' : '💾 Save Settings'}
                    </button>
                </div>
            </div>
        </div>
    );
}
