import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import quizService from "../services/quizService";

/* =========================
   TIPOVI
========================= */

type Answer = {
  id: string;
  tekst: string;
};

type Question = {
  id: number;
  tekst: string;
  bodovi: number;
  odgovori: Answer[];
};

type PlayableQuiz = {
  id: string;
  naziv: string;
  pitanja: Question[];
  trajanje_sekunde: number;
};

type PlayerAnswer = {
  pitanje_id: number;
  odgovor_ids: string[];
};

/* =========================
   KOMPONENTA
========================= */

const PlayQuiz = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState<PlayableQuiz | null>(null);
  const [answers, setAnswers] = useState<PlayerAnswer[]>([]);
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [startedAt, setStartedAt] = useState<number>(0);
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    const loadQuiz = async () => {
      try {
        const data = await quizService.getById(id!);
        setQuiz(data);
        setTimeLeft(data.trajanje_sekunde);
        setStartedAt(Date.now());
      } catch (err) {
        alert("Greška pri učitavanju kviza");
        navigate("/dashboard");
      }
    };

    loadQuiz();
  }, [id, navigate]);

  
  useEffect(() => {
    if (!timeLeft || finished) return;

    const timer = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timer);
          submitQuiz();
          return 0;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, finished]);

  
  const toggleAnswer = (questionId: number, answerId: string) => {
    setAnswers((prev) => {
      const existing = prev.find(
        (a) => a.pitanje_id === questionId
      );

      if (!existing) {
        return [
          ...prev,
          { pitanje_id: questionId, odgovor_ids: [answerId] },
        ];
      }

      const alreadySelected = existing.odgovor_ids.includes(answerId);

      const updatedIds = alreadySelected
        ? existing.odgovor_ids.filter((id) => id !== answerId)
        : [...existing.odgovor_ids, answerId];

      return prev.map((a) =>
        a.pitanje_id === questionId
          ? { ...a, odgovor_ids: updatedIds }
          : a
      );
    });
  };

  const submitQuiz = async () => {
    if (finished || !quiz) return;

    setFinished(true);

    const timeSpent = Math.floor(
      (Date.now() - startedAt) / 1000
    );

    try {
      await quizService.submit(id!, answers, timeSpent);
      alert("✅ Kviz je završen. Rezultati će stići na email.");
      navigate("/dashboard");
    } catch (err) {
      alert("Greška pri slanju odgovora");
    }
  };

   if (!quiz) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p>Učitavanje kviza...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8 space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">{quiz.naziv}</h2>
            <span className="text-red-600 font-semibold">
              ⏱ {timeLeft}s
            </span>
          </div>

          {quiz.pitanja.map((p) => {
            const selected =
              answers.find((a) => a.pitanje_id === p.id)
                ?.odgovor_ids || [];

            return (
              <div
                key={p.id}
                className="border rounded p-4 space-y-3"
              >
                <h3 className="font-semibold">{p.tekst}</h3>

                {p.odgovori.map((o) => (
                  <label
                    key={o.id}
                    className="flex items-center gap-2 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selected.includes(o.id)}
                      onChange={() =>
                        toggleAnswer(p.id, o.id)
                      }
                    />
                    <span>{o.tekst}</span>
                  </label>
                ))}
              </div>
            );
          })}

          <button
            onClick={submitQuiz}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Završi kviz
          </button>
        </div>
      </div>
    </div>
  );
};

export default PlayQuiz;
