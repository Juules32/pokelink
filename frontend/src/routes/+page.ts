export const ssr = false

import { fetchPuzzle } from '$lib/backend';

export async function load({ fetch, params }) {
    return {
        puzzleResponse: await fetchPuzzle(fetch, params)
    }
};
