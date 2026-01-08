import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import quizService from "../services/quizService";
import type { Quiz } from "../models/Quiz";

const SelectQuizForLeaderboard = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    quizService.getAll().then(setQuizzes);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">
            Izaberi kviz – rang lista
          </h2>

          {quizzes.map(q => (
            <div
              key={q.id}
              className="border rounded p-4 mb-3 flex justify-between items-center"
            >
              <div>
                <p className="font-semibold">{q.naziv}</p>
                <p className="text-sm text-gray-500">Status: {q.status}</p>
              </div>

              <button
                onClick={() => navigate(`/kvizovi/${q.id}/leaderboard`)}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Rang lista
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SelectQuizForLeaderboard;
