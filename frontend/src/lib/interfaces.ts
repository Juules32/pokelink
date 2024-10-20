export interface SearchResult {
	name: string;
	url: string;
}

export interface PokemonNode {
	id: number;
	name: string;
	types: string[];
	region: string;
}

export interface AdjacencyData {
	guess: PokemonNode;
	adjacentPokemon: PokemonNode[];
}

export interface Puzzle {
	source: PokemonNode;
	target: PokemonNode;
	shortestPath: PokemonNode[];
	shortestPathLength: number;
}
