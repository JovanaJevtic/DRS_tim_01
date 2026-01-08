export type QuizStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface Quiz {
  id: string;
  naziv: string;
  status: QuizStatus;
  autor_id: number;
  autor_email: string;
  razlog_odbijanja?: string;
  created_at?: string;
}
