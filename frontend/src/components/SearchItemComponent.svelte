<script lang="ts">
    import type { PokemonNode } from '$lib/interfaces';
    import { edges } from '$lib/state';
    import { addNode } from '$lib/state';
    import { getSpriteUrl } from '$lib/util';
    import { guessedNodes } from '$lib/state';

    export let pokemonNode: PokemonNode;
    export let resetSearch: Function;


    function tryGuess() {
        const latestGuess = $guessedNodes.at(-1)?.name;
        if (latestGuess) {
            if(edges[latestGuess].includes(pokemonNode.name)) {
                addNode(pokemonNode.name)
            }
        }
        resetSearch()
    }
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img src={getSpriteUrl(pokemonNode.id)} alt={pokemonNode.name} class="height-[96px] width-[20px]" />
    <p class="grow text-left pl-2 capitalize truncate">{pokemonNode.name}</p>
    <button on:click={tryGuess} class="rounded-md px-4 py-2 bg-red-400">Guess</button>
</li>
