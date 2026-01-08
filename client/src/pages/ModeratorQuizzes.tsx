import { useEffect, useState } from "react";
import quizService from "../services/quizService";
import type { Quiz } from "../models/Quiz";

const ModeratorQuizzes = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);

  // =========================
  // UČITAJ MOJE KVIZOVE
  // =========================
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

  // =========================
  // OBRIŠI KVIZ
  // =========================
  const deleteQuiz = async (id: string) => {
    const confirmed = window.confirm(
      "Da li si sigurna da želiš da obrišeš ovaj kviz?"
    );

    if (!confirmed) return;

    try {
      await quizService.delete(id);
      setQuizzes((prev) => prev.filter((q) => q.id !== id));
    } catch (err) {
      alert("Greška pri brisanju kviza");
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
      <div className="max-w-6xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Moji kvizovi</h2>

          {quizzes.length === 0 && (
            <p className="text-gray-600">Nemaš kreiranih kvizova.</p>
          )}

          <div className="space-y-4">
            {quizzes.map((q) => (
              <div
                key={q.id}
                className="border rounded-lg p-4 flex justify-between items-start"
              >
                <div>
                  <p className="text-lg font-semibold">{q.naziv}</p>
                  <p className="text-sm text-gray-600">
                    Status: <span className="font-medium">{q.status}</span>
                  </p>

                  {q.razlog_odbijanja && (
                    <p className="mt-2 text-sm text-red-600">
                      Razlog odbijanja: {q.razlog_odbijanja}
                    </p>
                  )}
                </div>

                {/* AKCIJE */}
                <div className="flex gap-2">
                  <button
                    onClick={() => deleteQuiz(q.id)}
                    className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    Obriši
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModeratorQuizzes;
