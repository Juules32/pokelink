import { isNameLegal } from '$lib/util'
import type { Pokemon } from '$lib/interfaces'

// Function to fetch the list of Pokémon and filter based on search query
export async function fetchSearchData(search: string): Promise<Pokemon[]> {
	try {
		const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
		const data = await response.json()
		const searchLowerCase = search.toLowerCase()
		const filteredResponse = data.results
			.filter((pokemon: Pokemon) => isNameLegal(pokemon.name))
			.filter((pokemon: Pokemon) => pokemon.name.includes(searchLowerCase))
			.sort((a: Pokemon, b: Pokemon) => customSort(a, b, searchLowerCase))
			.slice(0, 10)

		const spriteUrls: Pokemon[] = await Promise.all(
			filteredResponse.map(async (pokemon: Pokemon) => {
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
function customSort(a: Pokemon, b: Pokemon, searchLowerCase: string): number {
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
