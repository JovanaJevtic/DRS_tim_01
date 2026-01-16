import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LOCK_TIME_MS = 60_000;

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const [attempts, setAttempts] = useState<Record<string, number>>({});
  const [lockUntil, setLockUntil] = useState<number | null>(null);
  const [secondsLeft, setSecondsLeft] = useState(0);

  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    if (!lockUntil) return;

    const interval = setInterval(() => {
      const remaining = Math.ceil((lockUntil - Date.now()) / 1000);

      if (remaining <= 0) {
        setLockUntil(null);
        setSecondsLeft(0);
        setError('');
      } else {
        setSecondsLeft(remaining);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [lockUntil]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (lockUntil) return;

    setLoading(true);
    setError('');

    const email = formData.email.trim().toLowerCase();

    if (!email.includes('@')) {
      setError('Unesite ispravan email');
      setLoading(false);
      return;
    }

    const domain = email.split('@')[1];
    const ALLOWED_EMAIL_DOMAINS = [
      'gmail.com',
      'hotmail.com',
      'outlook.com',
      'live.com',
      'yahoo.com',
      'icloud.com',
      'protonmail.com',
      'proton.me',
      'uns.ac.rs',
    ];

    if (!ALLOWED_EMAIL_DOMAINS.includes(domain)) {
      setError('Unesite ispravan email');
      setLoading(false);
      return;
    }

    try {
      const result = await login(email, formData.password);

      if (result.success) {
        setAttempts(prev => ({ ...prev, [email]: 0 }));
        navigate('/dashboard');
      } else {
        const currentAttempts = (attempts[email] ?? 0) + 1;

        setAttempts(prev => ({
          ...prev,
          [email]: currentAttempts,
        }));

        if (currentAttempts >= 3) {
          setError('Pogrešna lozinka. Pristup je privremeno zabranjen.');
          setLockUntil(Date.now() + LOCK_TIME_MS);
          setSecondsLeft(60);
        } else {
          setError('Pogrešna lozinka');
        }
      }
    } catch {
      setError('Greška pri prijavljivanju');
    } finally {
      setLoading(false);
    }
  };

  const isLocked = !!lockUntil;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Prijavite se na nalog
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ili{' '}
            <Link
              to="/register"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              registrujte se za novi nalog
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
              <div>{error}</div>
              {isLocked && (
                <div className="mt-1 font-semibold">
                  Pokušajte ponovo za {secondsLeft}s
                </div>
              )}
            </div>
          )}

          <div className="rounded-md shadow-sm space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email adresa
              </label>
              <input
                name="email"
                type="email"
                required
                disabled={isLocked}
                value={formData.email}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="ime@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lozinka
              </label>
              <input
                name="password"
                type="password"
                required
                disabled={isLocked}
                value={formData.password}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || isLocked}
            className="w-full flex justify-center py-2 px-4 rounded-md text-white bg-primary-600 disabled:opacity-50"
          >
            {loading ? 'Prijavljivanje...' : 'Prijavi se'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
