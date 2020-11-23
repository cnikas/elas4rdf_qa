export interface Answer {
  answer: string;
  type: string;
  entity: string;
  similarity: number
}

export interface Entity {
	uri: string;
	rdfsComment: string;
}

export interface Response {
  question: string;
  category: string;
  types: string[];
  entities: Entity[];
  answers: Answer[];
}