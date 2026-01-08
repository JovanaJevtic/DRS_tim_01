export type PlayableAnswer = {
  id: string;
  tekst: string;
};

export type PlayableQuestion = {
  id: number;
  tekst: string;
  bodovi: number;
  odgovori: PlayableAnswer[];
};

export interface PlayableQuiz {
  id: string;
  naziv: string;
  pitanja: PlayableQuestion[];
  trajanje_sekunde: number;
}
