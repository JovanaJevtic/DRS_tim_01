import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import quizService from "../services/quizService";

const AvailableQuizzes = () => {
  const [quizzes, setQuizzes] = useState<any[]>([]);

  useEffect(() => {
    quizService.getAll("APPROVED").then(setQuizzes);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Dostupni kvizovi</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quizzes.map(q => (
              <div
                key={q.id}
                className="border rounded-lg p-6 flex justify-between items-center"
              >
                <p className="text-lg font-semibold">{q.naziv}</p>
                <Link
                  to={`/kvizovi/${q.id}/play`}
                  className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                >
                  Igraj
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AvailableQuizzes;
