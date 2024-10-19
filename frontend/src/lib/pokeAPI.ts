import { isNameLegal } from '$lib/util'
import type { SearchResult } from '$lib/interfaces'

// Function to fetch the list of Pokémon and filter based on search query
export async function fetchSearchData(search: string): Promise<SearchResult[]> {
	try {
		const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
		const data = await response.json()
		const searchLowerCase = search.toLowerCase()
		const filteredResponse = data.results
			.filter((pokemon: SearchResult) => isNameLegal(pokemon.name))
			.filter((pokemon: SearchResult) => pokemon.name.includes(searchLowerCase))
			.sort((a: SearchResult, b: SearchResult) => customSort(a, b, searchLowerCase))
			.slice(0, 10)

		const spriteUrls: SearchResult[] = await Promise.all(
			filteredResponse.map(async (pokemon: SearchResult) => {
				const spriteUrl = await getPokemonSprite(pokemon.url)
				return { name: pokemon.name, url: spriteUrl }
			})
		)

		return spriteUrls
	} catch (error) {
		console.error(error)
		return []
	}
}

// Helper function for custom sorting
function customSort(a: SearchResult, b: SearchResult, searchLowerCase: string): number {
	const startsWithSearchStringA = a.name.toLowerCase().startsWith(searchLowerCase)
	const startsWithSearchStringB = b.name.toLowerCase().startsWith(searchLowerCase)

	if (startsWithSearchStringA && !startsWithSearchStringB) {
		return -1
	} else if (!startsWithSearchStringA && startsWithSearchStringB) {
		return 1
	} else {
		return a.name.localeCompare(b.name)
	}
}

// Fetch the Pokémon sprite from a given URL
async function getPokemonSprite(url: string) : Promise<string> {
	try {
		const response = await fetch(url)
		const data = await response.json()
		return data.sprites.front_default
	} catch (error) {
		console.error(error)
		return ""
	}
}
