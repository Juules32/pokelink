import { fetchPuzzle } from '$lib/backend';

export async function load({ fetch }) {
    return {
        puzzleSolution: await fetchPuzzle(fetch, undefined)
    }
};
