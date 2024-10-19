<script lang="ts">
    import type { Node } from "$lib/interfaces";

    export let pokemonNode: Node;

    const circleDiameter = 128;
</script>

<div
    style="background-image: url(https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemonNode.id}.png);"
    class="min-h-[{circleDiameter}px] min-w-[{circleDiameter}px] border-black border-2 bg-white p-[10px] h-[{circleDiameter}px] w-[{circleDiameter}px] opacity-0 rounded-full text-center whitespace-nowrap transition-opacity duration-500 bg-center pt-4 bg-no-repeat guessed-pokemon-node text-wrap leading-3 capitalize flex flex-col justify-between items-center"
>
    <p>
        {pokemonNode.name}
    </p>
    <div class="flex justify-center pixel gap-1">
        {#each pokemonNode.types as type}
            <img src="types/{type}.png" alt={type} />
        {/each}
    </div>
</div>
