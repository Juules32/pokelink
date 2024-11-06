import { fetchNumPuzzles, fetchPuzzles } from '$lib/backend';

export async function load({ fetch, url }) {
    const pageQueryParameter = url.searchParams.get("page")
    const pageNum = pageQueryParameter ? parseInt(pageQueryParameter) : 1

    return {
        puzzles: await fetchPuzzles(fetch, pageNum),
        numPuzzles: await fetchNumPuzzles(fetch),
        pageNum: pageNum
    }
};
