export interface BankQuestion {
    question: string;
    options: [string, string, string, string];
    correct_index: 0 | 1 | 2 | 3;
    explanation: string;
}

export type Difficulty = 'beginner' | 'intermediate' | 'advanced';
export type SubjectBank = Record<Difficulty, BankQuestion[]>;
