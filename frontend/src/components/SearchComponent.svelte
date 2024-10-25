<script lang="ts">
    import SearchItemComponent from "$components/SearchItemComponent.svelte";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { PokemonNode } from "$lib/interfaces";
    import { pokemonNodes } from "$lib/state";

    let searchQuery = $state("");
    let filteredPokemonNodes: PokemonNode[] = $state([]);
    let searchRef: HTMLElement | null = $state(null);
    interface Props {
        tryGuess: Function;
    }

    let { tryGuess }: Props = $props();

    // Filter and return search results based on search query
    function getSearchData(search: string): PokemonNode[] {
        const searchLowerCase = search.toLowerCase();
        return pokemonNodes
            .filter((node: PokemonNode) => node.name.includes(searchLowerCase))
            .sort((a: PokemonNode, b: PokemonNode) =>
                customSort(a, b, searchLowerCase)
            )
            .slice(0, 10);
    }

    // Helper function for custom sorting
    function customSort(a: PokemonNode, b: PokemonNode, searchLowerCase: string): number {
        const startsWithSearchStringA = a.name.toLowerCase().startsWith(searchLowerCase);
        const startsWithSearchStringB = b.name.toLowerCase().startsWith(searchLowerCase);

        // Prioritizes names that start with the search string
        if (startsWithSearchStringA && !startsWithSearchStringB) {
            return -1;
        } 
        else if (!startsWithSearchStringA && startsWithSearchStringB) {
            return 1;
        } 
        // Otherwise, items are sorted alphabetically
        else {
            return a.name.localeCompare(b.name);
        }
    }

    function handleClickOutside(event: MouseEvent) {
        // If the click is outside the input field, clear pokemonNodes
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

<div class="z-20 w-3/4 max-w-[500px]" bind:this={searchRef}>
    <div
        class="bg-red-400 h-16 flex border-2 border-black justify-center items-center rounded-lg"
        class:rounded-b-none={searchQuery}
    >
        <input
            class="p-2 border-2 w-3/4 max-w-[292px] border-black"
            type="text"
            bind:value={searchQuery}
            oninput={async () => {
                filteredPokemonNodes = getSearchData(searchQuery);
            }}
            placeholder="Search Pokémon..."
        />
    </div>
    {#if searchQuery}
        <ul
            class="z-10 absolute w-3/4 sm:w-[500px] divide-y divide-dashed h-96 overflow-y-auto border-2 border-t-0 border-black bg-white rounded-b-lg"
        >
            {#each filteredPokemonNodes as pokemonNode}
                <SearchItemComponent {resetSearch} {pokemonNode} {tryGuess} />
            {/each}
        </ul>
    {/if}
</div>
