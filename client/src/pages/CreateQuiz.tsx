import { useState } from "react";
import { useNavigate } from "react-router-dom";
import quizService from "../services/quizService";

type Answer = {
  id: string;
  tekst: string;
  tacan: boolean;
};

type Question = {
  id: number;
  tekst: string;
  bodovi: number;
  odgovori: Answer[];
};

const CreateQuiz = () => {
  const navigate = useNavigate();

  const [naziv, setNaziv] = useState("");
  const [trajanje, setTrajanje] = useState(60);
  const [pitanja, setPitanja] = useState<Question[]>([]);

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // =========================
  // VALIDACIJA (BACKEND MIRROR)
  // =========================
  const validate = (): boolean => {
    // Naziv
    if (!naziv.trim()) {
      setError("Naziv kviza je obavezan");
      return false;
    }

    if (naziv.trim().length < 3) {
      setError("Naziv mora imati najmanje 3 karaktera");
      return false;
    }

    // Pitanja
    if (!pitanja || pitanja.length === 0) {
      setError("Kviz mora imati bar jedno pitanje");
      return false;
    }

    // Trajanje
    if (!trajanje || trajanje < 10) {
      setError("Trajanje mora biti najmanje 10 sekundi");
      return false;
    }

    // Validacija svakog pitanja
    for (let i = 0; i < pitanja.length; i++) {
      const p = pitanja[i];

      if (!p.tekst.trim()) {
        setError(`Pitanje ${i + 1}: Tekst je obavezan`);
        return false;
      }

      if (!p.bodovi || p.bodovi <= 0) {
        setError(`Pitanje ${i + 1}: Bodovi moraju biti veći od 0`);
        return false;
      }

      const odgovori = p.odgovori || [];
      if (odgovori.length < 2) {
        setError(`Pitanje ${i + 1}: Mora imati najmanje 2 odgovora`);
        return false;
      }

      const imaTacan = odgovori.some(o => o.tacan);
      if (!imaTacan) {
        setError(`Pitanje ${i + 1}: Mora imati bar jedan tačan odgovor`);
        return false;
      }

      for (const o of odgovori) {
        if (!o.tekst.trim()) {
          setError(`Pitanje ${i + 1}: Svi odgovori moraju imati tekst`);
          return false;
        }
      }
    }

    setError(null);
    return true;
  };

  // =========================
  // PITANJA
  // =========================
  const addQuestion = () => {
    setPitanja(prev => [
      ...prev,
      {
        id: prev.length + 1,
        tekst: "",
        bodovi: 10,
        odgovori: [
          { id: crypto.randomUUID(), tekst: "", tacan: false },
          { id: crypto.randomUUID(), tekst: "", tacan: false },
        ],
      },
    ]);
  };

  const updateQuestionText = (index: number, tekst: string) => {
    const copy = [...pitanja];
    copy[index] = { ...copy[index], tekst };
    setPitanja(copy);
  };

  const updateQuestionPoints = (index: number, bodovi: number) => {
    const copy = [...pitanja];
    copy[index] = { ...copy[index], bodovi };
    setPitanja(copy);
  };

  // =========================
  // ODGOVORI
  // =========================
  const updateAnswerText = (qIndex: number, aIndex: number, tekst: string) => {
    const copy = [...pitanja];
    copy[qIndex].odgovori[aIndex] = {
      ...copy[qIndex].odgovori[aIndex],
      tekst,
    };
    setPitanja(copy);
  };

  const toggleAnswerCorrect = (qIndex: number, aIndex: number) => {
    const copy = [...pitanja];
    copy[qIndex].odgovori[aIndex] = {
      ...copy[qIndex].odgovori[aIndex],
      tacan: !copy[qIndex].odgovori[aIndex].tacan,
    };
    setPitanja(copy);
  };

  const addAnswer = (qIndex: number) => {
    const copy = [...pitanja];
    copy[qIndex].odgovori.push({
      id: crypto.randomUUID(),
      tekst: "",
      tacan: false,
    });
    setPitanja(copy);
  };

  // =========================
  // SUBMIT
  // =========================
  const submit = async () => {
    if (!validate()) return;

    await quizService.create({
      naziv,
      trajanje_sekunde: trajanje,
      pitanja,
    });

    setSuccess("✅ Kviz je uspešno sačuvan");

    setTimeout(() => {
      navigate("/kvizovi/moji");
    }, 1200);
  };

  // =========================
  // UI
  // =========================
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-10 px-4">
        <div className="bg-white shadow-xl rounded-lg p-8 space-y-6">
          <h2 className="text-2xl font-bold">Kreiraj kviz</h2>

          {error && (
            <div className="bg-red-100 text-red-700 px-4 py-2 rounded">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-100 text-green-700 px-4 py-2 rounded">
              {success}
            </div>
          )}

          <input
            className="w-full border rounded px-4 py-2"
            placeholder="Naziv kviza"
            value={naziv}
            onChange={(e) => setNaziv(e.target.value)}
          />

          <input
            type="number"
            className="w-full border rounded px-4 py-2"
            placeholder="Trajanje (sekunde)"
            value={trajanje}
            onChange={(e) => setTrajanje(Number(e.target.value))}
          />

          <hr />

          {pitanja.map((p, qIndex) => (
            <div key={p.id} className="border rounded p-4 space-y-3">
              <h3 className="font-semibold">Pitanje {qIndex + 1}</h3>

              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Tekst pitanja"
                value={p.tekst}
                onChange={(e) =>
                  updateQuestionText(qIndex, e.target.value)
                }
              />

              <input
                type="number"
                className="w-full border rounded px-3 py-2"
                placeholder="Bodovi"
                value={p.bodovi}
                onChange={(e) =>
                  updateQuestionPoints(qIndex, Number(e.target.value))
                }
              />

              {p.odgovori.map((o, aIndex) => (
                <div key={o.id} className="flex gap-2 items-center">
                  <input
                    className="flex-1 border rounded px-3 py-2"
                    placeholder={`Odgovor ${aIndex + 1}`}
                    value={o.tekst}
                    onChange={(e) =>
                      updateAnswerText(qIndex, aIndex, e.target.value)
                    }
                  />
                  <input
                    type="checkbox"
                    checked={o.tacan}
                    onChange={() =>
                      toggleAnswerCorrect(qIndex, aIndex)
                    }
                  />
                  <span>Tačan</span>
                </div>
              ))}

              <button
                onClick={() => addAnswer(qIndex)}
                className="text-sm text-blue-600 hover:underline"
              >
                + Dodaj odgovor
              </button>
            </div>
          ))}

          <button
            onClick={addQuestion}
            className="w-full bg-gray-200 py-2 rounded hover:bg-gray-300"
          >
            + Dodaj pitanje
          </button>

          <button
            onClick={submit}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Sačuvaj kviz
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateQuiz;
