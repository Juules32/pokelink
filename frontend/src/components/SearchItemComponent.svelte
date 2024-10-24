<script lang="ts">
    import type { PokemonNode } from "$lib/interfaces";
    import { getSpriteUrl } from "$lib/util";

    export let pokemonNode: PokemonNode;
    export let tryGuess: Function;
    export let resetSearch: Function;
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img
        src={getSpriteUrl(pokemonNode.id)}
        alt={pokemonNode.name}
        class="height-[96px] width-[20px]"
    />
    <p class="grow text-left pl-2 capitalize truncate">{pokemonNode.name}</p>
    <button
        on:click={() => {
            tryGuess(pokemonNode.name);
            resetSearch();
        }}
        class="rounded-md px-4 py-2 bg-red-400">Guess</button
    >
</li>
