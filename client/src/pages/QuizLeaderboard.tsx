import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import quizService from "../services/quizService";

type LeaderboardEntry = {
  igrac_email: string;
  bodovi: number;
  vrijeme_utroseno: number;
};

const QuizLeaderboard = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [results, setResults] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadLeaderboard = async () => {
      try {
        const data = await quizService.leaderboard(id!);
        setResults(data);
      } catch (err) {
        alert("Greška pri učitavanju rang liste");
        navigate("/dashboard");
      } finally {
        setLoading(false);
      }
    };

    loadLeaderboard();
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p>Učitavanje rang liste...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Rang lista</h2>

          {results.length === 0 ? (
            <p className="text-gray-600">
              Još uvek nema rezultata za ovaj kviz.
            </p>
          ) : (
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-3 border">#</th>
                  <th className="p-3 border">Igrač</th>
                  <th className="p-3 border">Bodovi</th>
                  <th className="p-3 border">Vreme (s)</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r, index) => (
                  <tr
                    key={index}
                    className={index === 0 ? "bg-yellow-100" : ""}
                  >
                    <td className="p-3 border font-semibold">
                      {index + 1}
                    </td>
                    <td className="p-3 border">{r.igrac_email}</td>
                    <td className="p-3 border">{r.bodovi}</td>
                    <td className="p-3 border">{r.vrijeme_utroseno}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <button
            onClick={() => navigate(-1)}
            className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Nazad
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizLeaderboard;
