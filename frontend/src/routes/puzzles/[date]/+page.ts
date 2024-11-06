import { fetchPuzzle } from '$lib/backend';

export const ssr = false

export async function load({ fetch, params }) {
    return {
        puzzleSolution: await fetchPuzzle(fetch, params.date)
    }
};
