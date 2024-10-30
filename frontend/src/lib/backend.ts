import type { GraphData, Puzzle, PuzzlesItem } from "$lib/interfaces";
import { PUBLIC_BACKEND_HOST } from '$env/static/public'
import { error } from "@sveltejs/kit";

class HttpError extends Error {
    status: number;
    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

export async function fetchPuzzle(
    fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>,
    params: Record<string, string>
): Promise<Puzzle> {
    try {
        const endpoint = params.date ? "puzzle/" + params.date : "puzzle";
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/${endpoint}`)
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data);
            error.status = response.status;  // Attach the status to the error object
            throw error;  // This will be caught in the .catch() block
        }

        const result: Puzzle = {
            date: data.date,
            source: data.source,
            target: data.target,
            shortestPath: data.shortest_path,
            shortestPathLength: data.shortest_path_length
        }
        return result
    }
    catch (err) {
        if (err instanceof HttpError) {
            error(err.status, err.message)
        }
        error(500, "Could not fetch puzzle")
    }
}

export async function fetchHint(source: string, target: string): Promise<string> {
    try {
        const response = await fetch(
            `${PUBLIC_BACKEND_HOST}/hint?source=${source}&target=${target}`
        )
        const data = await response.json()
        return data
    }
    catch {
        error(500, "Could not fetch hint")
    }
}

export async function fetchGraphData(): Promise<GraphData> {
    try {
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/graph_data`)
        const data = await response.json()
        return data
    }
    catch {
        error(500, "Could not fetch graph data")
    }
}

export async function fetchPuzzles(
    fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>
): Promise<PuzzlesItem[]> {
    try {
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/puzzles?userid=2`)
        if (!response.ok) {
            throw new Error()
        }
        const data = await response.json()
        return data
    }
    catch {
        error(500, "Could not fetch puzzles")
    }
}
