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

export interface PuzzleResponse {
	puzzle: Puzzle;
	solution: string[] | null;
}
