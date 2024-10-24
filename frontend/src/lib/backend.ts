import type { GraphData, Puzzle } from "$lib/interfaces";
import { PUBLIC_BACKEND_HOST } from '$env/static/public'
import { error } from "@sveltejs/kit";

export async function fetchPuzzle(fetch: any, params: any): Promise<Puzzle> {
    try {
        let endpoint = params.slug ? "puzzle/" + params.slug : "puzzle";
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/${endpoint}`)
        if (!response.ok) {
            throw new Error()
        }
        const data = await response.json()
        const result: Puzzle = {
            source: data.source,
            target: data.target,
            shortestPath: data.shortest_path,
            shortestPathLength: data.shortest_path_length
        }
        return result
    }
    catch {
        error(404, "No puzzle could be found")
    }
}

export async function fetchHint(source: string, target: string): Promise<string> {
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/hint?source=${source}&target=${target}`)
    const data = await response.json()
    return data
}

export async function fetchGraphData(): Promise<GraphData> {
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/graph_data`)
    const data = await response.json()
    return data
}
