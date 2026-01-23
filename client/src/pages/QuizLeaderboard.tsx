import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import quizService from "../services/quizService";
import { useAuth } from "../context/AuthContext";

type LeaderboardEntry = {
  igrac_email: string;
  bodovi: number;
  vrijeme_utroseno: number;
};


type QuizInfo = {
  id: string;
  naziv: string;
  status?: string; 
  [key: string]: any;
};

const QuizLeaderboard = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [results, setResults] = useState<LeaderboardEntry[]>([]);
  const [quizStatus, setQuizStatus] = useState<string>("");
  const [quizNaziv, setQuizNaziv] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [pdfLoading, setPdfLoading] = useState(false);

  useEffect(() => {
    const loadLeaderboard = async () => {
      try {
        const data = await quizService.leaderboard(id!);
        setResults(data);
          
        const quizData: QuizInfo = await quizService.getById(id!);
        setQuizStatus(quizData.status || "APPROVED"); 
        setQuizNaziv(quizData.naziv || "");
      } catch (err) {
        console.error("Greška pri učitavanju:", err);
        alert("Greška pri učitavanju rang liste");
        navigate("/dashboard");
      } finally {
        setLoading(false);
      }
    };

    loadLeaderboard();
  }, [id, navigate]);

  const generatePdfReport = async () => {
    if (!id) return;
    try {
      setPdfLoading(true);
      await quizService.generateReport(id);
      alert("✅ PDF izvještaj je poslat na vaš email.");
    } catch (e) {
      console.error("Greška pri generisanju PDF-a:", e);
      alert("❌ Greška pri generisanju PDF izvještaja");
    } finally {
      setPdfLoading(false);
    }
  };

  
  const canGeneratePdf = user?.uloga === "ADMINISTRATOR" && 
                         (quizStatus === "APPROVED" || !quizStatus);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold">Rang lista</h2>
              {quizNaziv && (
                <p className="text-sm text-gray-600 mt-1">{quizNaziv}</p>
              )}
              {quizStatus && (
                <p className="text-xs text-gray-500 mt-1">
                  Status: <span className="font-medium">{quizStatus}</span>
                </p>
              )}
            </div>

            {/* PDF dugme SAMO za ADMINISTRATORA i SAMO za ODOBRENE kvizove */}
            {canGeneratePdf && (
              <button
                onClick={generatePdfReport}
                disabled={pdfLoading}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition"
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
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                  />
                </svg>
                {pdfLoading ? "Generišem..." : "Izvezi PDF"}
              </button>
            )}
          </div>

          {results.length === 0 ? (
            <div className="text-center py-8">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
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
              <p className="mt-2 text-gray-600">
                Još uvek nema rezultata za ovaj kviz.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100 text-left">
                    <th className="p-3 border font-semibold">#</th>
                    <th className="p-3 border font-semibold">Igrač</th>
                    <th className="p-3 border font-semibold">Bodovi</th>
                    <th className="p-3 border font-semibold">Vreme (s)</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r, index) => (
                    <tr
                      key={index}
                      className={`${
                        index === 0 
                          ? "bg-yellow-100" 
                          : index % 2 === 0 
                          ? "bg-gray-50" 
                          : "bg-white"
                      }`}
                    >
                      <td className="p-3 border font-semibold">
                        {index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : index + 1}
                      </td>
                      <td className="p-3 border">{r.igrac_email}</td>
                      <td className="p-3 border font-medium">{r.bodovi}</td>
                      <td className="p-3 border">{r.vrijeme_utroseno}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <button
            onClick={() => navigate(-1)}
            className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition flex items-center gap-2"
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
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Nazad
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizLeaderboard;
