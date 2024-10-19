<script lang="ts">
    import type { Node } from "$lib/interfaces";

    // Props
    export let pokemonNode: Node;
    export let circleDiameter: number;

    // Dictionary with soft colors for each Pokémon type
    const typeColors: { [key: string]: string } = {
        bug: "#A6B91A",
        dark: "#705746",
        dragon: "#6F35FC",
        electric: "#F7D02C",
        fairy: "#D685AD",
        fighting: "#C22E28",
        fire: "#EE8130",
        flying: "#A98FF3",
        ghost: "#735797",
        grass: "#7AC74C",
        ground: "#E2BF65",
        ice: "#96D9D6",
        normal: "#A8A77A",
        poison: "#A33EA1",
        psychic: "#F95587",
        rock: "#B6A136",
        steel: "#B7B7CE",
        water: "#6390F0"
    };

    // Function to create the gradient based on Pokémon types
    function getGradientFromTypes(types: string[]): string {
        if (types.length === 1) {
            const color = typeColors[types[0]];
            return `linear-gradient(45deg, ${color}, ${color} 100%)`;
        } else if (types.length === 2) {
            const color1 = typeColors[types[0]];
            const color2 = typeColors[types[1]];
            return `linear-gradient(45deg, ${color1}, ${color2})`;
        }

        // Default gradient if no types found
        return `linear-gradient(45deg, #A8A77A, #A8A77A)`;
    }

    const gradient = getGradientFromTypes(pokemonNode.types);
</script>

<div
    style="background-image: url(https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemonNode.id}.png), {gradient};"
    class="min-h-[{circleDiameter}px] min-w-[{circleDiameter}px] border-black bg-white h-[{circleDiameter}px] w-[{circleDiameter}px] rounded-full bg-center bg-no-repeat guessed-pokemon-node text-wrap leading-3 capitalize flex flex-col justify-between items-center"
>
    <p
        class="bg-white text-black rounded-md border-black border-2 p-1 text-center whitespace-nowrap truncate max-w-[{circleDiameter}px]"
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
