import { fetchPuzzle } from '$lib/backend';

// TODO: Instead, fetch the puzzle dates and set them here
export function entries() {
	return [
		{ slug: '2024-10-23' },
		{ slug: '2024-10-24' },
		{ slug: '2024-10-25' }
	];
}

export async function load({ fetch, params }) {
    return {
        puzzle: await fetchPuzzle(fetch, params)
    }
};
