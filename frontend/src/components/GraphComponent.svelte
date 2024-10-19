<script lang="ts">
    import NodeComponent from "./NodeComponent.svelte";
    import { puzzle, updateState } from "$lib/state";
    import { guessedNodes } from "$lib/state";
    import { fetchPuzzle } from "$lib/backend";
    import { onMount } from "svelte";

    // Constants
    const gapSize = 10;
    const circleDiameter = 128;

    // The graph width changes dynamically
    let graphWidth: number;

    // The total offset changes dynamically
    let totalOffset = 0;
    $: totalOffset = $guessedNodes.length * (circleDiameter + gapSize);

    async function setupPuzzle() {
        $puzzle = await fetchPuzzle();
        updateState($puzzle.source);
    }

    onMount(() => {
        setupPuzzle();
    });
</script>

<div
    class="bg-red-400 w-3/4 py-4 h-[160px] rounded-lg border-black border-2 overflow-hidden"
    bind:clientWidth={graphWidth}
>
    <div
        class="flex transition-transform duration-500"
        style:gap="{gapSize}px"
        style="transform: translateX({Math.abs(totalOffset) > graphWidth
            ? graphWidth - totalOffset
            : gapSize}px);"
    >
        {#each $guessedNodes as guessedNode}
            <NodeComponent pokemonNode={guessedNode} {circleDiameter} />
        {/each}
    </div>
</div>

<!-- Debugging Button -->
<button on:click={() => updateState("butterfree")}>Add Butterfree</button>
