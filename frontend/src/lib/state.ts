import type { PokemonBlob } from "$lib/interfaces";
import { fetchAdjacencyData } from "$lib/backend";
import { writable } from 'svelte/store';

export const guessedPokemonBlobs = writable<PokemonBlob[]>([]);

export async function addGuessBlob(guess: string) {
    const newBlob: PokemonBlob = await fetchAdjacencyData(guess)
    guessedPokemonBlobs.update((blobs) => [...blobs, newBlob]);
    console.log(guessedPokemonBlobs)
}
