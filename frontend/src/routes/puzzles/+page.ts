import { fetchNumPuzzles, fetchPuzzles } from '$lib/backend';
import { getFormattedDate } from '$lib/util.js';

export async function load({ fetch, url }) {
    const pageQueryParameter = url.searchParams.get("page")
    const pageNum = pageQueryParameter ? parseInt(pageQueryParameter) : 1
    const userdate = getFormattedDate();

    return {
        puzzles: await fetchPuzzles(fetch, userdate, pageNum),
        numPuzzles: await fetchNumPuzzles(fetch, userdate),
        pageNum: pageNum
    }
};
