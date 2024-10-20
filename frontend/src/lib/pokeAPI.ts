import { isNameLegal } from '$lib/util'
import type { SearchResult } from '$lib/interfaces'
import { get, writable } from 'svelte/store';

const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
const data = await response.json()
const pokemonResults: SearchResult[] = data.results
export const validResults: SearchResult[] = pokemonResults.filter((pokemon) => isNameLegal(pokemon.name));
export const localUrls = writable<{ [key: string]: string }>({});

// Fetch the Pokémon sprite from a given URL
export async function getPokemonSprite(url: string) : Promise<string> {
	try {
		const response = await fetch(url)
		const data = await response.json()
		return data.sprites.front_default
	} catch (error) {
		console.error(error)
		return ""
	}
}

// Fetches and stores name to url data locally
export async function prefetchSprites() {
	// Set local url data if it already exists
	const localUrlData = localStorage.getItem("spriteUrls")
	if (localUrlData) {
		localUrls.set(JSON.parse(localUrlData))
	}

	// Otherwise, fetch sprite urls and set them
	else {
		await Promise.all(
			validResults.map(async (pokemon: SearchResult) => {
				const spriteUrl = await getPokemonSprite(pokemon.url)
				get(localUrls)[pokemon.name] = spriteUrl;
			})
		)

		// Caches urls
		localStorage.setItem("spriteUrls", JSON.stringify(get(localUrls)))
	}
}
