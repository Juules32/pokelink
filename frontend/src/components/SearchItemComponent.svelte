<script lang="ts">
    import type { SearchResult } from '$lib/interfaces';
    import { updateState, validGuesses } from '$lib/state';
    export let searchResult: SearchResult;
    export let resetSearch: Function;

    function tryGuess() {
        if ($validGuesses.some(node => node.name == searchResult.name)) {
            updateState(searchResult.name)
        }
        resetSearch()
    }
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img src={searchResult.url} alt={searchResult.name} class="height-[96px] width-[20px]" />
    <p class="grow text-left pl-2 capitalize truncate">{searchResult.name}</p>
    <button on:click={tryGuess} class="rounded-md px-4 py-2 bg-red-400">Guess</button>
</li>
