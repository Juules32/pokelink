<script lang="ts">
    import SearchItemComponent from "$components/SearchItemComponent.svelte";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { PokemonNode } from "$lib/interfaces";
    import { pokemonNodes } from "$lib/globals";

    interface Props {
        tryGuess: (name: string) => void;
    }
    let { tryGuess }: Props = $props();

    const searchGuess = (name: string) => {
        tryGuess(name);
        resetSearch();
        searchInput?.focus();
    };

    let searchQuery = $state("");
    let filteredPokemonNodes: PokemonNode[] = $state([]);

    // The outermost div of the search component
    let searchRef: HTMLElement | undefined = $state();

    // The input element of the search component
    let searchInput: HTMLInputElement | undefined = $state();

    // Filter and return search results based on search query
    function getSearchData(search: string): PokemonNode[] {
        const searchLowerCase = search.toLowerCase();
        return $pokemonNodes
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

    function handleSubmit(event: Event) {
        event.preventDefault();
        const firstItem = filteredPokemonNodes[0]?.name;
        if (firstItem) {
            searchGuess(firstItem);
        }
    }

    let width = $state();
</script>

<div class="z-30 w-full" bind:this={searchRef} bind:clientWidth={width}>
    <div
        class="bg-red-400 h-16 flex border-2 border-black justify-center items-center rounded-lg"
        class:rounded-b-none={searchQuery}
    >
        <form class="w-3/4 max-w-[292px]" onsubmit={handleSubmit}>
            <input
                class="p-2 border-2 w-full border-black"
                type="text"
                bind:value={searchQuery}
                bind:this={searchInput}
                oninput={async () => {
                    filteredPokemonNodes = getSearchData(searchQuery);
                }}
                placeholder="Search Pokémon..."
            />
        </form>
    </div>
    {#if searchQuery}
        <ul
            style="width: {width}px;"
            class="z-10 absolute divide-y divide-dashed divide-gray-300 h-96 overflow-y-auto border-2 border-t-0 border-black bg-white rounded-b-lg"
        >
            {#each filteredPokemonNodes as pokemonNode}
                <SearchItemComponent {searchGuess} {pokemonNode} />
            {/each}
        </ul>
    {/if}
</div>
