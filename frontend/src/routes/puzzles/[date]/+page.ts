import { fetchPuzzle } from '$lib/backend';
import { getFormattedDate } from '$lib/util.js';

export async function load({ fetch, params }) {
    return {
        puzzleSolution: await fetchPuzzle(fetch, params.date, getFormattedDate())
    }
};
