import { fetchPuzzles } from '$lib/backend';

export async function load({ fetch }) {
    return {
        puzzles: await fetchPuzzles(fetch)
    }
};
