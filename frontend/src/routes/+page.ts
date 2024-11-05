export const ssr = false

import { fetchPuzzle } from '$lib/backend';

export async function load({ fetch }) {
    return {
        puzzleResponse: await fetchPuzzle(fetch, undefined)
    }
};
