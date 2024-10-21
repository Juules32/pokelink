import type { GraphData, PokemonNode, Puzzle } from "$lib/interfaces";
import { PUBLIC_BACKEND_HOST } from '$env/static/public'

console.log(PUBLIC_BACKEND_HOST)

export async function fetchPuzzle(): Promise<Puzzle> {
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/puzzle`)
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
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/hint?source=${source}&target=${target}`)
    const data = await response.json()
    return data
}

export async function fetchGraphData(): Promise<GraphData> {
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/graph_data`)
    const data = await response.json()
    return data
}
