import type { AdjacencyData, PokemonNode, Puzzle } from "$lib/interfaces";

// Function to fetch the list of Pokémon and filter based on search query
export async function fetchAdjacencyData(guess: string): Promise<AdjacencyData> {
	const response = await fetch(`http://localhost/adjacency_data/${guess}`)
    const data = await response.json()
    const result: AdjacencyData = {
        guess: data.guess,
        adjacentPokemon: data.adjacent_pokemon
    }
    return result
}

export async function fetchPuzzle(): Promise<Puzzle> {
    const response = await fetch(`http://localhost/puzzle`)
    const data = await response.json()
    const result: Puzzle = {
        source: data.source,
        target: data.target,
        shortestPath: data.shortest_path,
        shortestPathLength: data.shortest_path_length
    }
    return result
}

export async function fetchHint(source: string, target: string): Promise<PokemonNode> {
    const response = await fetch(`http://localhost/hint?source=${source}&target=${target}`)
    const data = await response.json()
    return data
}
