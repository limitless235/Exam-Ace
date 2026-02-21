import { BrowserRouter, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import QuizStart from './pages/QuizStart';
import QuizTake from './pages/QuizTake';
import Results from './pages/Results';
import Settings from './pages/Settings';
import Performance from './pages/Performance';

function Navbar() {
  const { user, signOut } = useAuth();
  const location = useLocation();

  if (!user) return null;

  const isActive = (path: string) => location.pathname.startsWith(path) ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/dashboard" className="navbar-brand">
          ExamAce
        </Link>
        <div className="navbar-links">
          <Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link>
          <Link to="/quiz/start" className={isActive('/quiz')}>Quiz</Link>
          <Link to="/performance" className={isActive('/performance')}>Performance</Link>
          <Link to="/settings" className={isActive('/settings')}>Settings</Link>
          <button onClick={signOut} style={{ color: 'var(--error)' }}>Sign Out</button>
        </div>
      </div>
    </nav>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="page">
        <div className="container loading-state">
          <div className="spinner" />
          <p>Loading…</p>
        </div>
      </div>
    );
  }

  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/quiz/start" element={<ProtectedRoute><QuizStart /></ProtectedRoute>} />
        <Route path="/quiz/:id" element={<ProtectedRoute><QuizTake /></ProtectedRoute>} />
        <Route path="/results/:id" element={<ProtectedRoute><Results /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
        <Route path="/performance" element={<ProtectedRoute><Performance /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
