<script lang="ts">
    import { base } from "$app/paths";
    import type { PokemonNode } from "$lib/interfaces";

    // Props
    export let pokemonNode: PokemonNode;
    export let circleDiameter = 128;
    export let isSecret = false;

    // Dictionary with soft colors for each Pokémon type in RGB format
    const typeColors: { [key: string]: string } = {
        bug: "rgb(166, 185, 26)",
        dark: "rgb(112, 87, 70)",
        dragon: "rgb(111, 53, 252)",
        electric: "rgb(247, 208, 44)",
        fairy: "rgb(214, 133, 173)",
        fighting: "rgb(194, 46, 40)",
        fire: "rgb(238, 129, 48)",
        flying: "rgb(169, 143, 243)",
        ghost: "rgb(115, 87, 151)",
        grass: "rgb(122, 199, 76)",
        ground: "rgb(226, 191, 101)",
        ice: "rgb(150, 217, 214)",
        normal: "rgb(168, 167, 122)",
        poison: "rgb(163, 62, 161)",
        psychic: "rgb(249, 85, 135)",
        rock: "rgb(182, 161, 54)",
        steel: "rgb(183, 183, 206)",
        water: "rgb(99, 144, 240)"
    };

    // Function to create the gradient based on Pokémon types
    function getGradientFromTypes(types: string[]): string {
        if (types.length == 1) {
            const color = typeColors[types[0]];
            return `linear-gradient(45deg, ${color}, ${color} 100%)`;
        } else if (types.length == 2) {
            const color1 = typeColors[types[0]];
            const color2 = typeColors[types[1]];
            return `linear-gradient(45deg, ${color1}, ${color2})`;
        }

        // Default gradient if no types found
        return `linear-gradient(45deg, rgb(168, 167, 122), rgb(168, 167, 122))`;
    }
</script>

<div
    style="min-height: {circleDiameter}px; min-width: {circleDiameter}px; width: {circleDiameter}px; height: {circleDiameter}px; background-image: {getGradientFromTypes(pokemonNode.types)};"
    class="z-10 border-black bg-white rounded-full bg-center bg-no-repeat guessed-pokemon-node text-wrap leading-3 capitalize flex flex-col justify-between items-center"
>
    <p
        style="max-width: {circleDiameter}px;"
        class="bg-white text-black rounded-md border-black border-2 p-1 truncate"
    >
        {#if isSecret}
            ???
        {:else}
            {pokemonNode.name}
        {/if}
    </p>
    <div
        style="transform: translateY(-{96 / 2}px);"
        class="sticky overflow-visible h-0 top-0"
    >
        <img
            class="drop-shadow-xl"
            style={isSecret ? "filter: brightness(0%);" : ""}
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemonNode.id}.png"
            alt="sprite"
        />
    </div>
    <div
        class="z-10 flex justify-center pixel gap-1 bg-white rounded-md border-black border-2 p-[2px]"
    >
        {#each pokemonNode.types as type}
            <img
                src="{base}/types/{isSecret ? 'unknown' : type}.png"
                alt={type}
            />
        {/each}
    </div>
</div>
