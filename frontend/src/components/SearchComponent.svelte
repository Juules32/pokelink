<script lang="ts">
    import type { SearchResult } from "$lib/interfaces";
    import SearchItemComponent from "$components/SearchItemComponent.svelte";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import { getPokemonSprite, localUrls, validResults } from "$lib/pokeAPI";

    let searchQuery = "";
    let searchResults: SearchResult[] = [];
    let searchRef: HTMLElement | null = null;
    
    // Filter and return search results based on search query
    async function fetchSearchData(search: string): Promise<SearchResult[]> {
        try {
            const searchLowerCase = search.toLowerCase()
            const filteredResponse = validResults
                .filter((pokemon: SearchResult) => pokemon.name.includes(searchLowerCase))
                .sort((a: SearchResult, b: SearchResult) => customSort(a, b, searchLowerCase))
                .slice(0, 10)
                
            const spriteUrls: SearchResult[] = await Promise.all(
                filteredResponse.map(async (pokemon: SearchResult) => {
                    const preFetchedUrl = $localUrls[pokemon.name]
                    let spriteUrl: string
                    if (preFetchedUrl) {
                        spriteUrl = $localUrls[pokemon.name]
                    }
                    else {
                        console.log(`Sprite url for ${pokemon.name} wasn't present locally, fetching from pokeAPI...`)
                        spriteUrl = await getPokemonSprite(pokemon.url)
                    }
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

        // Prioritizes names that start with the search string
        if (startsWithSearchStringA && !startsWithSearchStringB) {
            return -1
        } else if (!startsWithSearchStringA && startsWithSearchStringB) {
            return 1

        // Otherwise, items are sorted alphabetically
        } else {
            return a.name.localeCompare(b.name)
        }
    }

    function handleClickOutside(event: MouseEvent) {
        // If the click is outside the input field, clear searchResults
        if (searchRef && !searchRef.contains(event.target as Node)) {
            resetSearch();
        }
    }

    function resetSearch() {
        searchQuery = "";
    }

    onMount(() => {
        if (browser) document.addEventListener("click", handleClickOutside);
    });

    onDestroy(() => {
        if (browser) document.removeEventListener("click", handleClickOutside);
    });
</script>

<div class="w-3/4" bind:this={searchRef}>
    <div
        class="bg-red-400 h-16 flex border-2 border-black justify-center items-center rounded-lg"
        class:rounded-b-none={searchQuery}
    >
        <input
            class="p-2 border-2 w-3/4 border-black"
            type="text"
            bind:value={searchQuery}
            on:input={async () => {searchResults = await fetchSearchData(searchQuery)}}
            placeholder="Search Pokémon..."
        />
    </div>
    {#if searchQuery}
        <ul
            class="z-10 absolute w-3/4 divide-y divide-dashed h-96 overflow-y-auto border-2 border-t-0 border-black bg-white rounded-b-lg"
        >
            {#each searchResults as searchResult}
                <SearchItemComponent {searchResult} {resetSearch} />
            {/each}
        </ul>
    {/if}
</div>

<style scoped>
    ::-webkit-scrollbar {
        width: 12px;
    }

    ::-webkit-scrollbar-track {
        background-color: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #888;
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background-color: #555;
    }
</style>
