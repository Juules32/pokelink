import { fetchPuzzle } from '$lib/backend';
import { getFormattedDate } from '$lib/util';

export async function load({ fetch }) {
    const date = getFormattedDate();
    return {
        puzzleSolution: await fetchPuzzle(fetch, date, date)
    }
};
