<script lang="ts">
    import type { Pokemon } from "$lib/interfaces";
    import { fetchSearchData } from "$lib/pokeAPI";
    import SearchResult from "$components/SearchResult.svelte";

    let searchQuery = "";
    let pokemonResults: Pokemon[] = [];

    async function fetchSearchDataWrapper() {
        pokemonResults = await fetchSearchData(searchQuery);
    }
</script>

<div class="w-[500px] mt-32 h-fit">
    <div
        class="bg-red-400 h-16 flex border-2 border-b-0 border-black justify-center items-center rounded-t-lg"
    >
        <input
            class="p-2 w-72 border-2 border-black"
            type="text"
            bind:value={searchQuery}
            on:input={fetchSearchDataWrapper}
            placeholder="Search Pokémon..."
        />
    </div>
    <ul
        class="divide-y divide-dashed h-96 overflow-y-auto border-2 border-black bg-white rounded-b-lg"
    >
        {#each pokemonResults as pokemon}
            <SearchResult name={pokemon.name} url={pokemon.url} />
        {/each}
    </ul>
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
