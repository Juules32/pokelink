<script lang="ts">
    import type { PokemonNode } from "$lib/interfaces";
    import { getSpriteUrl } from "$lib/util";

    interface Props {
        pokemonNode: PokemonNode;
        tryGuess: Function;
        resetSearch: Function;
    }

    let { pokemonNode, tryGuess, resetSearch }: Props = $props();
</script>

<li class="hover:bg-gray-200 flex items-center align-middle p-2">
    <img
        src={getSpriteUrl(pokemonNode.id)}
        alt={pokemonNode.name}
        class="height-[96px] width-[20px]"
    />
    <p class="grow text-left pl-2 capitalize truncate">{pokemonNode.name}</p>
    <button
        onclick={() => {
            tryGuess(pokemonNode.name);
            resetSearch();
        }}
        class="rounded-md px-4 py-2 bg-red-400">Guess</button
    >
</li>
