<script lang="ts">
    import { addGuessBlob } from '$lib/state';
    export let pokemonSearchResult;
    export let resetSearch;
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img src={pokemonSearchResult.url} alt={pokemonSearchResult.name} class="height-[96px] width-[20px]" />
    <p class="grow text-left pl-2 capitalize">{pokemonSearchResult.name}</p>
    <button on:click={() => {addGuessBlob(pokemonSearchResult.name); resetSearch()}} class="rounded-md px-4 py-2 bg-red-400">Guess</button>
</li>
