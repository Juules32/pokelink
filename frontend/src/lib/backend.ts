import type { Node, Puzzle } from "$lib/interfaces";

// Function to fetch the list of Pokémon and filter based on search query
export async function fetchAdjacencyData(guess: string): Promise<Node> {
	const response = await fetch(`http://localhost/adjacency_data/${guess}`)
    const data = await response.json()
    const result: Node = {
        name: data.guess.name,
        id: data.guess.id,
        types: data.guess.types,
        region: data.guess.region
    }
    return result
}

export async function fetchPuzzle(): Promise<Puzzle> {
    const response = await fetch(`http://localhost/puzzle`)
    const data = await response.json()
    console.log(data)
    const result: Puzzle = data
    return result
}
