export interface PokemonSearchResult {
	name: string;
	url: string;
}

export interface PokemonBlob {
	id: number;
	name: string;
	types: string[];
	region: string;
}

export interface Puzzle {
	source: string;
	target: string;
	shortestPath: string[];
	shortestPathLength: number;
}
