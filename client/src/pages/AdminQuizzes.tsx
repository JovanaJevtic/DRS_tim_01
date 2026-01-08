import { useEffect, useState } from "react";
import quizService from "../services/quizService";

const AdminQuizzes = () => {
  const [quizzes, setQuizzes] = useState<any[]>([]);

  useEffect(() => {
    quizService.getAll().then(setQuizzes);
  }, []);

  const refresh = async () => {
    setQuizzes(await quizService.getAll());
  };

  const approve = async (id: string) => {
    await quizService.approve(id);
    refresh();
  };

  const reject = async (id: string) => {
    const razlog = prompt("Razlog odbijanja:");
    if (!razlog) return;
    await quizService.reject(id, razlog);
    refresh();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Svi kvizovi</h2>

          <div className="space-y-4">
            {quizzes.map(q => (
              <div
                key={q.id}
                className="border rounded-lg p-4 flex flex-col md:flex-row md:items-center md:justify-between"
              >
                <div>
                  <p className="text-lg font-semibold">{q.naziv}</p>
                  <span
                    className={`text-sm font-medium ${
                      q.status === "APPROVED"
                        ? "text-green-600"
                        : q.status === "REJECTED"
                        ? "text-red-600"
                        : "text-yellow-600"
                    }`}
                  >
                    {q.status}
                  </span>
                </div>

                {q.status === "PENDING" && (
                  <div className="mt-4 md:mt-0 flex gap-2">
                    <button
                      onClick={() => approve(q.id)}
                      className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => reject(q.id)}
                      className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminQuizzes;
