import { useEffect, useState } from "react";
import quizService from "../services/quizService";
import type { Quiz } from "../models/Quiz";

type Answer = {
  id: string;
  tekst: string;
  tacan?: boolean;
};

type Question = {
  id: number;
  tekst: string;
  bodovi: number;
  odgovori: Answer[];
};

type QuizPreview = Quiz & {
  pitanja: Question[];
  trajanje_sekunde: number;
};

const AdminQuizzes = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [selectedQuiz, setSelectedQuiz] = useState<QuizPreview | null>(null);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQuizzes();
  }, []);

  const loadQuizzes = async () => {
    setLoading(true);
    const data = await quizService.getAll();
    setQuizzes(data);
    setLoading(false);
  };

  const handlePreview = async (quiz: Quiz) => {
    try {
      const fullQuiz = await quizService.getById(quiz.id);
      setSelectedQuiz(fullQuiz as QuizPreview);
      setShowPreviewModal(true);
    } catch (err) {
      console.error("Greška pri učitavanju kviza:", err);
      alert("Greška pri učitavanju kviza");
    }
  };

  const approve = async (id: string) => {
    const confirmed = window.confirm("Da li ste sigurni da želite da odobrite ovaj kviz?");
    if (!confirmed) return;

    await quizService.approve(id);
    setShowPreviewModal(false);
    loadQuizzes();
  };

  const reject = async (id: string) => {
    const razlog = prompt("Unesite razlog odbijanja:");
    if (!razlog || razlog.trim() === "") {
      alert("Razlog odbijanja je obavezan!");
      return;
    }

    await quizService.reject(id, razlog);
    setShowPreviewModal(false);
    loadQuizzes();
  };

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
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Svi kvizovi</h2>
            <div className="text-sm text-gray-600">
              Ukupno: <span className="font-semibold">{quizzes.length}</span>
            </div>
          </div>

          {quizzes.length === 0 ? (
            <p className="text-gray-600 text-center py-8">Nema kreiranih kvizova.</p>
          ) : (
            <div className="space-y-4">
              {quizzes.map((q) => (
                <div
                  key={q.id}
                  className="border rounded-lg p-4 hover:shadow-md transition"
                >
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <p className="text-lg font-semibold">{q.naziv}</p>
                        <span
                          className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusBadge(
                            q.status
                          )}`}
                        >
                          {q.status}
                        </span>
                      </div>

                      {q.autor_email && (
                        <p className="text-sm text-gray-600">
                          Autor: <span className="font-medium">{q.autor_email}</span>
                        </p>
                      )}

                      {q.razlog_odbijanja && (
                        <p className="mt-2 text-sm text-red-600">
                          Razlog odbijanja: {q.razlog_odbijanja}
                        </p>
                      )}
                    </div>

                    <div className="flex gap-2 flex-wrap">
                      <button
                        onClick={() => handlePreview(q)}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition flex items-center gap-2"
                      >
                        <svg
                          className="w-4 h-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                          />
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                          />
                        </svg>
                        Pregledaj
                      </button>

                      {q.status === "PENDING" && (
                        <>
                          <button
                            onClick={() => approve(q.id)}
                            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
                          >
                            Odobri
                          </button>
                          <button
                            onClick={() => reject(q.id)}
                            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
                          >
                            Odbij
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* PREVIEW MODAL */}
      {showPreviewModal && selectedQuiz && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
          <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="sticky top-0 bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-t-lg">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-2xl font-bold mb-2">{selectedQuiz.naziv}</h3>
                  <div className="flex gap-3 text-sm">
                    <span className="bg-white bg-opacity-20 px-3 py-1 rounded">
                      ⏱ {selectedQuiz.trajanje_sekunde}s
                    </span>
                    <span className="bg-white bg-opacity-20 px-3 py-1 rounded">
                      📝 {selectedQuiz.pitanja?.length || 0} pitanja
                    </span>
                    <span
                      className={`px-3 py-1 rounded font-semibold ${
                        selectedQuiz.status === "APPROVED"
                          ? "bg-green-500"
                          : selectedQuiz.status === "REJECTED"
                          ? "bg-red-500"
                          : "bg-yellow-500"
                      }`}
                    >
                      {selectedQuiz.status}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setShowPreviewModal(false)}
                  className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="p-6 space-y-6">
              {selectedQuiz.pitanja && selectedQuiz.pitanja.length > 0 ? (
                selectedQuiz.pitanja.map((pitanje, index) => (
                  <div
                    key={pitanje.id}
                    className="border-2 border-gray-200 rounded-lg p-5 bg-gray-50"
                  >
                    {/* Pitanje Header */}
                    <div className="flex justify-between items-start mb-4">
                      <h4 className="text-lg font-semibold text-gray-900">
                        <span className="text-purple-600">Pitanje {index + 1}:</span>{" "}
                        {pitanje.tekst}
                      </h4>
                      <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium ml-4 flex-shrink-0">
                        {pitanje.bodovi} bodova
                      </span>
                    </div>

                    {/* Odgovori */}
                    <div className="space-y-2">
                      {pitanje.odgovori && pitanje.odgovori.length > 0 ? (
                        pitanje.odgovori.map((odgovor, oIndex) => (
                          <div
                            key={odgovor.id}
                            className={`flex items-center gap-3 p-3 rounded-lg border-2 ${
                              odgovor.tacan
                                ? "bg-green-50 border-green-400"
                                : "bg-white border-gray-200"
                            }`}
                          >
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-sm font-medium">
                              {String.fromCharCode(65 + oIndex)}
                            </span>
                            <span
                              className={`flex-1 ${
                                odgovor.tacan ? "font-semibold text-green-900" : "text-gray-700"
                              }`}
                            >
                              {odgovor.tekst}
                            </span>
                            {odgovor.tacan && (
                              <span className="flex-shrink-0 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                                ✓ TAČAN
                              </span>
                            )}
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-500 italic">Nema odgovora</p>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-8">Nema pitanja u ovom kvizu.</p>
              )}

              {/* Razlog odbijanja */}
              {selectedQuiz.razlog_odbijanja && (
                <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4">
                  <p className="text-red-800 font-semibold">Razlog odbijanja:</p>
                  <p className="text-red-700 mt-1">{selectedQuiz.razlog_odbijanja}</p>
                </div>
              )}
            </div>

            {/* Footer - Action Buttons */}
            {selectedQuiz.status === "PENDING" && (
              <div className="sticky bottom-0 bg-gray-100 p-6 rounded-b-lg flex gap-4">
                <button
                  onClick={() => approve(selectedQuiz.id)}
                  className="flex-1 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition font-semibold flex items-center justify-center gap-2"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  Odobri Kviz
                </button>
                <button
                  onClick={() => reject(selectedQuiz.id)}
                  className="flex-1 bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition font-semibold flex items-center justify-center gap-2"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                  Odbij Kviz
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminQuizzes;
