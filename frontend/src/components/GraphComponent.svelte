<script lang="ts">

    import NodeComponent from "./NodeComponent.svelte";
    import { addGuessNode } from "$lib/state"
    import { tick } from "svelte";
    import { guessedNodes } from "$lib/state";
    import { fetchPuzzle } from "$lib/backend";
    import type { Puzzle } from "$lib/interfaces";
    import { onMount } from "svelte";

    let wrapper: HTMLElement;

    let graphWidth: number;

    const gapSize = 10;

    // Keeps track of the total shift in X
    let totalOffset = 0;

    $: if ($guessedNodes.length) { 
        updateVisuals()
    };

    async function updateVisuals() {
        await tick();
        
        const lastItem: HTMLElement | null = wrapper.querySelector(
            ".guessed-pokemon-node:last-child"
        );
        if (lastItem) {
            const newOffsetAmount = lastItem.offsetWidth + gapSize;

            // Update the total offset to account for the new element's width
            totalOffset -= newOffsetAmount;

            // Set the opacity to completely visible
            // This triggers the opacity transition
            lastItem.style.opacity = "1";
        }
    }

    async function fetchPuzzleWrapper() {
        const puzzle: Puzzle = await fetchPuzzle()
        addGuessNode(puzzle.source)
    }

    onMount(() => {
        fetchPuzzleWrapper()
    })
</script>

<div
    class="bg-red-400 w-3/4 py-4 h-[160px] rounded-lg border-black border-2 overflow-hidden"
    bind:clientWidth={graphWidth}
>
    <div
        class="flex transition-transform duration-500"
        style:gap="{gapSize}px"
        style="transform: translateX({Math.abs(totalOffset) > graphWidth ? graphWidth + totalOffset : gapSize}px);"
        bind:this={wrapper}
    >
        {#each $guessedNodes as guessedNode}
            <NodeComponent pokemonNode={guessedNode} />
        {/each}
    </div>
</div>

<button on:click={() => addGuessNode("butterfree")}>Add Butterfree</button>
