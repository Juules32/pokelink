import { fetchPuzzle } from '$lib/backend';

export async function load({ fetch, params }) {
    return {
        puzzleSolution: await fetchPuzzle(fetch, params.date)
    }
};
