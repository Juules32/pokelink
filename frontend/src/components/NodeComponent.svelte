<script lang="ts">
    import type { PokemonNode } from "$lib/interfaces";

    // Props
    export let pokemonNode: PokemonNode;
    export let circleDiameter: number;

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
    style="min-height: {circleDiameter}px; min-width: {circleDiameter}px; width: {circleDiameter}px; height: {circleDiameter}px; background-image: url(https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemonNode.id}.png), {getGradientFromTypes(pokemonNode.types)};"
    class="border-black bg-white rounded-full bg-center bg-no-repeat guessed-pokemon-node text-wrap leading-3 capitalize flex flex-col justify-between items-center"
>
    <p
        style="max-width: {circleDiameter}px;"
        class="bg-white text-black rounded-md border-black border-2 p-1 truncate"
    >
        {pokemonNode.name}
    </p>
    <div
        class="flex justify-center pixel gap-1 bg-white rounded-md border-black border-2 p-[2px]"
    >
        {#each pokemonNode.types as type}
            <img src="types/{type}.png" alt={type} />
        {/each}
    </div>
</div>
