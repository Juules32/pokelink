import { fetchPuzzle } from '$lib/backend';

export async function load({ fetch, params }) {
    return {
        puzzle: await fetchPuzzle(fetch, params)
    }
};
