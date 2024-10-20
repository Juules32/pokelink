import type { AdjacencyData, PokemonNode, Puzzle } from "$lib/interfaces";
import { fetchAdjacencyData } from "$lib/backend";
import { get, writable } from 'svelte/store';

export const puzzle = writable<Puzzle>();

export const guessedNodes = writable<PokemonNode[]>([]);

export const validGuesses = writable<PokemonNode[]>([]);

// Adding local node data means the frontend can render before requesting
// new adjacency data from the backend, resulting in snappy updates.
function addLocalNode(guess: string) : boolean {
    const newNode = get(validGuesses).find((node) => node.name == guess)
    if (newNode) {
        guessedNodes.update((nodes) => [...nodes, newNode]);
        console.log("Loaded node data locally")
        return false
    }
    else {
        console.log("Failed to load data locally")
        return true
    }
}

export async function updateState(guess: string) {
    console.log(`Updating state for guess: ${guess}`)
    const failedLocal = addLocalNode(guess)
    const adjacencyData: AdjacencyData = await fetchAdjacencyData(guess)
    if (failedLocal) {
        guessedNodes.update((nodes) => [...nodes, adjacencyData.guess]);
        console.log("Loaded node data from backend instead")
    }
    validGuesses.set(adjacencyData.adjacentPokemon);

    if (get(puzzle).target.name == guess) {
        console.log("You win!")
    }
}
