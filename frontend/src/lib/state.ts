import type { Node } from "$lib/interfaces";
import { fetchAdjacencyData } from "$lib/backend";
import { writable } from 'svelte/store';

export const guessedNodes = writable<Node[]>([]);

export async function addGuessNode(guess: string) {
    const newNode: Node = await fetchAdjacencyData(guess)
    guessedNodes.update((nodes) => [...nodes, newNode]);
    console.log(guessedNodes)
}
