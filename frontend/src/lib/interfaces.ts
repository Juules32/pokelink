export interface SearchResult {
	name: string;
	url: string;
}

export interface Node {
	id: number;
	name: string;
	types: string[];
	region: string;
}

export interface AdjacencyData {
	guess: Node;
	adjacentPokemon: Node[];
}

export interface Puzzle {
	source: string;
	target: string;
	shortestPath: string[];
	shortestPathLength: number;
}
