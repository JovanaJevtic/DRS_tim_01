import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import type { RegisterData, Gender } from '../types';

const Register = () => {
  const [formData, setFormData] = useState<RegisterData>({
    ime: '',
    prezime: '',
    email: '',
    password: '',
    datum_rodjenja: '',
    pol: undefined,
    drzava: '',
    ulica: '',
    broj: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { register } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const validateForm = (): boolean => {
    // Obavezna polja
    if (!formData.ime || !formData.prezime || !formData.email || !formData.password) {
      setError('Ime, prezime, email i lozinka su obavezni');
      return false;
    }

    // Email validacija
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Unesite ispravan email');
      return false;
    }

    // Lozinka validacija
    if (formData.password.length < 6) {
      setError('Lozinka mora imati najmanje 6 karaktera');
      return false;
    }

    if (formData.password !== confirmPassword) {
      setError('Lozinke se ne poklapaju');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Priprema podataka za backend
      const registrationData: RegisterData = {
        ime: formData.ime,
        prezime: formData.prezime,
        email: formData.email,
        password: formData.password,
        datum_rodjenja: formData.datum_rodjenja || undefined,
        pol: formData.pol as Gender | undefined,
        drzava: formData.drzava || undefined,
        ulica: formData.ulica || undefined,
        broj: formData.broj || undefined,
      };

      const result = await register(registrationData);

      if (result.success) {
        navigate('/login', {
          state: { message: 'Uspešna registracija! Prijavite se.' },
        });
      } else {
        setError(result.message || 'Greška pri registraciji');
      }
    } catch (err) {
      setError('Greška pri registraciji. Pokušajte ponovo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Registrujte se
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Već imate nalog?{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
              Prijavite se
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Ime */}
            <div>
              <label htmlFor="ime" className="block text-sm font-medium text-gray-700 mb-1">
                Ime <span className="text-red-500">*</span>
              </label>
              <input
                id="ime"
                name="ime"
                type="text"
                required
                value={formData.ime}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Prezime */}
            <div>
              <label htmlFor="prezime" className="block text-sm font-medium text-gray-700 mb-1">
                Prezime <span className="text-red-500">*</span>
              </label>
              <input
                id="prezime"
                name="prezime"
                type="text"
                required
                value={formData.prezime}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Email */}
            <div className="md:col-span-2">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email <span className="text-red-500">*</span>
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Lozinka */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Lozinka <span className="text-red-500">*</span>
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Potvrda lozinke */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                Potvrdi lozinku <span className="text-red-500">*</span>
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Datum rođenja */}
            <div>
              <label htmlFor="datum_rodjenja" className="block text-sm font-medium text-gray-700 mb-1">
                Datum rođenja
              </label>
              <input
                id="datum_rodjenja"
                name="datum_rodjenja"
                type="date"
                value={formData.datum_rodjenja}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Pol */}
            <div>
              <label htmlFor="pol" className="block text-sm font-medium text-gray-700 mb-1">
                Pol
              </label>
              <select
                id="pol"
                name="pol"
                value={formData.pol || ''}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Izaberite</option>
                <option value="M">Muški</option>
                <option value="Z">Ženski</option>
                <option value="O">Drugo</option>
              </select>
            </div>

            {/* Država */}
            <div>
              <label htmlFor="drzava" className="block text-sm font-medium text-gray-700 mb-1">
                Država
              </label>
              <input
                id="drzava"
                name="drzava"
                type="text"
                value={formData.drzava}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Ulica */}
            <div>
              <label htmlFor="ulica" className="block text-sm font-medium text-gray-700 mb-1">
                Ulica
              </label>
              <input
                id="ulica"
                name="ulica"
                type="text"
                value={formData.ulica}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {/* Broj */}
            <div>
              <label htmlFor="broj" className="block text-sm font-medium text-gray-700 mb-1">
                Broj
              </label>
              <input
                id="broj"
                name="broj"
                type="text"
                value={formData.broj}
                onChange={handleChange}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Registracija...' : 'Registruj se'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;