<script lang="ts">
    import { addGuessNode } from '$lib/state';
    export let searchResult;
    export let resetSearch;
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img src={searchResult.url} alt={searchResult.name} class="height-[96px] width-[20px]" />
    <p class="grow text-left pl-2 capitalize">{searchResult.name}</p>
    <button on:click={() => {addGuessNode(searchResult.name); resetSearch()}} class="rounded-md px-4 py-2 bg-red-400">Guess</button>
</li>
