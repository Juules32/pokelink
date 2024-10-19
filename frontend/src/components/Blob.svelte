<script lang="ts">
    import type { PokemonBlob } from "$lib/interfaces";

    export let pokemonBlob: PokemonBlob;
</script>

<div
    style="background-image: url(https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemonBlob.id}.png);"
    class="border-black border-2 bg-white p-[10px] h-[128px] w-[128px] opacity-0 rounded-full text-center whitespace-nowrap transition-opacity duration-500 bg-center pt-4 bg-no-repeat guessed-pokemon-blob text-wrap leading-3 capitalize flex flex-col justify-between items-center"
>
    <p>
        {pokemonBlob.name}
    </p>
    <div class="flex justify-center pixel gap-1">
        {#each pokemonBlob.types as type}
            <img src="types/{type}.png" alt={type} />
        {/each}
    </div>
</div>
