import { useEffect, useState } from "react";
import quizService from "../services/quizService";

type MyResult = {
  quiz_id: string;
  quiz_naziv: string;
  ukupno_bodova: number;
  maksimalno_bodova: number;
  procenat: number;
  vrijeme_utroseno_sekunde: number;
  created_at?: string;
};

const QuizResults = () => {
  const [results, setResults] = useState<MyResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadResults = async () => {
      try {
        const data = await quizService.getMyResults();
        setResults(data);
      } catch {
        alert("Greška pri učitavanju rezultata");
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Učitavanje...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Moji rezultati</h2>

          {results.length === 0 ? (
            <p className="text-gray-600">
              Još uvek nemaš odigranih kvizova.
            </p>
          ) : (
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-3 border">Kviz</th>
                  <th className="p-3 border">Bodovi</th>
                  <th className="p-3 border">Procenat</th>
                  <th className="p-3 border">Vreme (s)</th>
                  <th className="p-3 border">Datum</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r, idx) => (
                  <tr key={idx}>
                    <td className="p-3 border">{r.quiz_naziv}</td>
                    <td className="p-3 border">
                      {r.ukupno_bodova}/{r.maksimalno_bodova}
                    </td>
                    <td className="p-3 border">
                      {r.procenat.toFixed(1)}%
                    </td>
                    <td className="p-3 border">
                      {r.vrijeme_utroseno_sekunde}
                    </td>
                    <td className="p-3 border">
                      {r.created_at
                        ? new Date(r.created_at).toLocaleString()
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizResults;
