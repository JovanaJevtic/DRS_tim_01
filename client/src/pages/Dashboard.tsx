import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import type { UserRole } from '../types';

const Dashboard = () => {
  const { user } = useAuth();

  const getRoleDescription = (role: UserRole): string => {
    switch (role) {
      case 'ADMINISTRATOR':
        return 'Administrator - puna kontrola nad platformom';
      case 'MODERATOR':
        return 'Moderator - kreiranje i upravljanje kvizovima';
      case 'IGRAC':
        return 'Igrač - igranje kvizova';
      default:
        return '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow-xl rounded-lg">
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Dobrodošli, {user?.email}!
            </h1>
            <p className="text-gray-600 mb-8">{user && getRoleDescription(user.uloga)}</p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Profil Card */}
              <Link
                to="/profile"
                className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold">Moj Profil</h3>
                  <svg
                    className="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </div>
                <p className="text-blue-100">Pogledajte i ažurirajte svoj profil</p>
              </Link>

              {/* Admin - Korisnici */}
              {user?.uloga === 'ADMINISTRATOR' && (
                <Link
                  to="/admin/users"
                  className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold">Korisnici</h3>
                    <svg
                      className="w-8 h-8"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                  </div>
                  <p className="text-purple-100">Upravljajte korisnicima platforme</p>
                </Link>
              )}

              {/* Moderator/Admin - Kvizovi */}
              {(user?.uloga === 'MODERATOR' || user?.uloga === 'ADMINISTRATOR') && (
                <Link
                  to="/kvizovi"
                  className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold">Kvizovi</h3>
                    <svg
                      className="w-8 h-8"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                  </div>
                  <p className="text-green-100">Kreirajte i upravljajte kvizovima</p>
                </Link>
              )}

              {/* Igrač - Dostupni Kvizovi */}
              {user?.uloga === 'IGRAC' && (
                <Link
                  to="/kvizovi/dostupni"
                  className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold">Dostupni Kvizovi</h3>
                    <svg
                      className="w-8 h-8"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                  <p className="text-yellow-100">Igrajte dostupne kvizove</p>
                </Link>
              )}

              {/* Rezultati */}
              {(user?.uloga === "IGRAC") && (

              <Link
                to="/kvizovi/rezultati"
                className="bg-gradient-to-br from-red-500 to-red-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold">Moji Rezultati</h3>
                  <svg
                    className="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <p className="text-red-100">Pregled vaših rezultata</p>
              </Link>
              )}

              {(user?.uloga === "ADMINISTRATOR" || user?.uloga === "MODERATOR") && (
                 <Link
                   to="/kvizovi/rang-liste"
                   className="bg-gradient-to-br from-red-500 to-red-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-shadow"
                 >
                   <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold">Rezultati</h3>
                  <svg
                    className="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <p className="text-red-100">Pregled rezultata</p>
                 </Link>
                )}

            </div>

            {/* Quick Stats */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gray-50 rounded-lg p-6">
                <h4 className="text-sm font-medium text-gray-500 uppercase">Status naloga</h4>
                <p className="mt-2 text-3xl font-semibold text-gray-900">Aktivan</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h4 className="text-sm font-medium text-gray-500 uppercase">Uloga</h4>
                <p className="mt-2 text-3xl font-semibold text-gray-900">{user?.uloga}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h4 className="text-sm font-medium text-gray-500 uppercase">Email</h4>
                <p className="mt-2 text-lg font-semibold text-gray-900 truncate">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;