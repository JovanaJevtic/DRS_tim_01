import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import quizService from "../services/quizService";
import type { Quiz } from "../models/Quiz";

const SelectQuizForLeaderboard = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadQuizzes = async () => {
      try {
        const data = await quizService.getAll();
        setQuizzes(data);
      } catch (err) {
        alert("Greška pri učitavanju kvizova");
      } finally {
        setLoading(false);
      }
    };
    
    loadQuizzes();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "APPROVED":
        return "bg-green-100 text-green-800";
      case "REJECTED":
        return "bg-red-100 text-red-800";
      case "PENDING":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p>Učitavanje...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">
            Izaberi kviz – rang lista
          </h2>

          {quizzes.length === 0 ? (
            <p className="text-gray-600">Nema dostupnih kvizova.</p>
          ) : (
            <div className="space-y-3">
              {quizzes.map((q) => (
                <div
                  key={q.id}
                  className="border rounded-lg p-4 flex justify-between items-center hover:bg-gray-50 transition"
                >
                  <div className="flex-1">
                    <p className="font-semibold text-lg">{q.naziv}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded ${getStatusBadge(
                          q.status
                        )}`}
                      >
                        {q.status}
                      </span>
                      {q.status === "REJECTED" && q.razlog_odbijanja && (
                        <span className="text-xs text-red-600">
                          (Razlog: {q.razlog_odbijanja})
                        </span>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={() => navigate(`/kvizovi/${q.id}/leaderboard`)}
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                  >
                    Rang lista
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SelectQuizForLeaderboard;
