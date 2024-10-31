import { fetchPuzzles } from '$lib/backend';

export const ssr = false

export async function load({ fetch }) {
    return {
        puzzles: await fetchPuzzles(fetch)
    }
};
