<script lang="ts">
    import NodeComponent from "./NodeComponent.svelte";
    import { puzzle, addNode } from "$lib/state";
    import { guessedNodes } from "$lib/state";
    import { fetchHint, fetchPuzzle } from "$lib/backend";
    import { onMount } from "svelte";
    import { pokemonNodes } from "$lib/state";
    import { graphData } from "$lib/state";
    import { regionNumber } from "$lib/util";

    // Constants
    const gapSize = 20;
    const circleDiameter = 128;

    // The graph width changes dynamically
    let graphWidth: number;

    // The offset changes dynamically
    let offsetX = 0;
    $: {
        offsetX = $guessedNodes.length * (circleDiameter + gapSize);
    }
    async function setupPuzzle() {
        $puzzle = await fetchPuzzle();
        addNode($puzzle.source);
    }

    let hint: string;
    async function getHint() {
        const latestGuessNode = $guessedNodes.at(-1)
        if (latestGuessNode)
            hint = await fetchHint(latestGuessNode.name, $puzzle.target)
        console.log(graphData.nodes[hint])
    }

    onMount(() => {
        setupPuzzle();
    });
</script>

<div
    class="bg-red-400 w-3/4 py-4 min-h-[150px] h-[150px] rounded-lg border-black border-2 overflow-hidden"
    bind:clientWidth={graphWidth}
>
    <div
        class="h-full flex items-center transition-transform duration-500"
        style="transform: translateX({Math.abs(offsetX) > graphWidth
            ? graphWidth - offsetX
            : gapSize}px);"
    >
        {#each $guessedNodes as guessedNode, i}
            {#if i}
                <p style="min-width: {gapSize}px;" class="text-lg text-center relative">→</p>
            {/if}
            <NodeComponent pokemonNode={guessedNode} {circleDiameter} />
        {/each}
    </div>
</div>

<!-- Debugging Button -->
<button on:click={() => addNode(pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)].name)}>Add Random Pokemon</button>

<button on:click={getHint}>Get Hint</button>

{#if hint}
    <NodeComponent pokemonNode={graphData.nodes[hint]} {circleDiameter} />
{/if}
