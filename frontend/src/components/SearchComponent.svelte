<script lang="ts">
    import type { SearchResult } from "$lib/interfaces";
    import { fetchSearchData } from "$lib/pokeAPI";
    import SearchItemComponent from "$components/SearchItemComponent.svelte";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";

    let searchQuery = "";
    let searchResults: SearchResult[] = [];
    let searchRef: HTMLElement | null = null;

    async function fetchSearchDataWrapper() {
        searchResults = await fetchSearchData(searchQuery);
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
            on:input={fetchSearchDataWrapper}
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
