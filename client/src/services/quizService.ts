import quizApi from "../api/quizAPI";
import type { Quiz } from "../models/Quiz";
import type { PlayableQuiz } from "../types/PlayableQuiz";

const quizService = {
  async getAll(status?: string): Promise<Quiz[]> {
    const res = await quizApi.get("/quiz/all", {
      params: status ? { status } : {},
    });
    return res.data.quizzes;
  },

  async getById(id: string): Promise<PlayableQuiz> {
    const res = await quizApi.get(`/quiz/${id}`);
    return res.data.quiz;
  },

  async create(data: {
    naziv: string;
    pitanja: any[];
    trajanje_sekunde: number;
  }): Promise<Quiz> {
    const res = await quizApi.post("/quiz/create", data);
    return res.data.quiz;
  },

  async delete(id: string): Promise<void> {
    await quizApi.delete(`/quiz/${id}`);
  },

  async approve(id: string): Promise<void> {
    await quizApi.patch(`/quiz/${id}/approve`);
  },

  async reject(id: string, razlog: string): Promise<void> {
    await quizApi.patch(`/quiz/${id}/reject`, { razlog });
  },

  async submit(
    quizId: string,
    odgovori: {
      pitanje_id: number;
      odgovor_id?: string;
      odgovor_ids?: string[];
    }[],
    vrijeme_utroseno_sekunde?: number
  ): Promise<any> {
    const res = await quizApi.post(`/quiz/${quizId}/submit`, {
      odgovori,
      vrijeme_utroseno_sekunde,
    });
    return res.data.result;
  },

  async leaderboard(quizId: string) {
    const res = await quizApi.get(`/quiz/${quizId}/leaderboard`);
    return res.data.leaderboard;
  },

  async generateReport(quizId: string): Promise<void> {
    await quizApi.post(`/quiz/${quizId}/report`);
  },

  async getMyResults() {
    const res = await quizApi.get("/quiz/my-results");
    return res.data.results;
  },
};

export default quizService;
