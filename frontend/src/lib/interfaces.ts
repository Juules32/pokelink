// The backend has corresponding pydantic models (but in snake case instead of pascal case)

export interface PokemonNode {
	name: string;
	id: number;
	types: string[];
	region: string;
}

export interface Puzzle {
	date: string;
	source: string;
	target: string;
	shortestPath: string[];
	shortestPathLength: number;
}

export interface GraphData {
	nodes: { [key: string]: PokemonNode };
	edges: { [key: string]: string[] };
}

export interface PuzzlesItem {
	date: string;
	source: string;
	target: string;
	completed: boolean;
}

export interface PuzzleSolution {
	puzzle: Puzzle;
	solution: string[] | null;
}
