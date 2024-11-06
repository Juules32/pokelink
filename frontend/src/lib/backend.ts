import type { GraphData, PuzzleSolution, PuzzlesItem } from "$lib/interfaces";
import { PUBLIC_BACKEND_HOST } from '$env/static/public'
import { error } from "@sveltejs/kit";
import { userid } from "./userid";

class HttpError extends Error {
    status: number;
    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}

export async function fetchPuzzle(
    fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>,
    date: string | undefined
): Promise<PuzzleSolution> {
    try {
        const endpoint = date ? "puzzle/" + date : "puzzle";
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/${endpoint}?userid=${userid}`)
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data.detail);
            throw error;
        }

        const result: PuzzleSolution = {
            puzzle: {
                date: data.puzzle.date,
                source: data.puzzle.source,
                target: data.puzzle.target,
                shortestPath: data.puzzle.shortest_path,
                shortestPathLength: data.puzzle.shortest_path_length
            },
            solution: data.solution
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

export async function fetchPuzzles(
    fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>,
    pageNum: number
): Promise<PuzzlesItem[]> {
    try {
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/puzzles?userid=${userid}&page=${pageNum}`)
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data.detail);
            throw error;
        }

        return data
    }
    catch (err) {
        if (err instanceof HttpError) {
            error(err.status, err.message)
        }
        error(500, "Could not fetch puzzles")
    }
}

export async function fetchNumPuzzles(
    fetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>
): Promise<number> {
    try {
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/num_puzzles`)
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data.detail);
            throw error;
        }

        return data
    }
    catch (err) {
        if (err instanceof HttpError) {
            error(err.status, err.message)
        }
        error(500, "Could not fetch number of puzzles")
    }
}


export async function fetchHint(source: string, target: string): Promise<string> {
    try {
        const response = await fetch(
            `${PUBLIC_BACKEND_HOST}/hint?source=${source}&target=${target}`
        )
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data.detail);
            throw error;
        }

        return data
    }
    catch (err) {
        if (err instanceof HttpError) {
            error(err.status, err.message)
        }
        error(500, "Could not fetch hint")
    }
}

export async function fetchGraphData(): Promise<GraphData> {
    try {
        const response = await fetch(`${PUBLIC_BACKEND_HOST}/graph_data`)
        const data = await response.json()

        if (!response.ok) {
            const error = new HttpError(response.status, data.detail);
            throw error;
        }

        return data
    }
    catch (err) {
        if (err instanceof HttpError) {
            error(err.status, err.message)
        }
        error(500, "Could not fetch graph data")
    }
}

export async function postSolution(date: string, guessedNames: string[]) {
    const response = await fetch(`${PUBLIC_BACKEND_HOST}/solution/${date}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ userid: userid, solution: guessedNames })
    });
    const data = await response.json()
    
    if (!response.ok) {
        const error = new HttpError(response.status, data.detail);
        throw error;
    }
}
