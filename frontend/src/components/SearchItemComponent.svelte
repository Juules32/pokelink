<script lang="ts">
    import type { PokemonNode } from "$lib/interfaces";
    import { getSpriteUrl } from "$lib/util";

    interface Props {
        pokemonNode: PokemonNode;
        searchGuess: (name: string) => void;
    }
    let { pokemonNode, searchGuess }: Props = $props();
</script>

<li class="transition-colors hover:bg-gray-300 flex items-center align-middle p-2">
    <img
        src={getSpriteUrl(pokemonNode.id)}
        alt={pokemonNode.name}
        class="height-[96px] width-[20px]"
    />
    <p class="grow text-left pl-2 capitalize truncate">{pokemonNode.name}</p>
    <button
        onclick={() => {
            searchGuess(pokemonNode.name);
        }}
        class="rounded-md px-4 py-2 bg-red-400 border-2 border-black"
    >
        Guess
    </button>
</li>
