import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const QuizDashboard = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-12 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Rad sa kvizovima
          </h1>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {user?.uloga === "ADMINISTRATOR" && (
              <Link
                to="/kvizovi/admin"
                className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition"
              >
                <h3 className="text-xl font-semibold mb-2">Svi kvizovi</h3>
                <p className="text-purple-100">
                  Pregled i odobravanje kvizova
                </p>
              </Link>
            )}

            {user?.uloga === "MODERATOR" && (
              <>
                <Link
                  to="/kvizovi/moji"
                  className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition"
                >
                  <h3 className="text-xl font-semibold mb-2">Moji kvizovi</h3>
                  <p className="text-green-100">
                    Upravljanje sopstvenim kvizovima
                  </p>
                </Link>

                <Link
                  to="/kvizovi/kreiraj"
                  className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition"
                >
                  <h3 className="text-xl font-semibold mb-2">Kreiraj kviz</h3>
                  <p className="text-blue-100">
                    Dodaj novi kviz na platformu
                  </p>
                </Link>
              </>
            )}

            {user?.uloga === "IGRAC" && (
              <Link
                to="/kvizovi/dostupni"
                className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition"
              >
                <h3 className="text-xl font-semibold mb-2">
                  Dostupni kvizovi
                </h3>
                <p className="text-yellow-100">
                  Igraj odobrene kvizove
                </p>
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizDashboard;
