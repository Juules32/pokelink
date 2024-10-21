export interface PokemonNode {
	name: string;
	id: number;
	types: string[];
	region: string;
}

export interface Puzzle {
	source: string;
	target: string;
	shortestPath: string[];
	shortestPathLength: number;
}

export interface GraphData {
	nodes: { [key: string]: PokemonNode };
	edges: { [key: string]: string[] }
}
