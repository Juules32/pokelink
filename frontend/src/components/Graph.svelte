<script lang="ts">

    import Blob from "./Blob.svelte";
    import { addGuessBlob } from "$lib/state"
    import { browser } from "$app/environment";
    import { tick } from "svelte";
    import { guessedPokemonBlobs } from "$lib/state";
    import { fetchPuzzle } from "$lib/backend";
    import type { Puzzle } from "$lib/interfaces";
    import { onMount } from "svelte";

    let wrapper: HTMLElement;
    const gapSize = 10;

    // Keeps track of the total shift in X
    let totalOffset = 0;

    if (browser) {
        // This should not use window width, but id = graphArea width
        totalOffset = 500;
    }

    $: if ($guessedPokemonBlobs.length) {
        updateVisuals()
    };

    async function updateVisuals() {
        await tick();
        
        const lastItem: HTMLElement | null = wrapper.querySelector(
            ".guessed-pokemon-blob:last-child"
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
        addGuessBlob(puzzle.source)
    }

    onMount(() => {
        fetchPuzzleWrapper()
    })
</script>

<div
    id="graphArea"
    class="bg-red-400 w-3/4 py-4 h-[160px] rounded-lg border-black border-2"
>
    <div id="gradient-mask" class="relative overflow-hidden flex items-center">
        <div
            class="flex transition-transform duration-500 gap-[{gapSize}px]"
            style="transform: translateX({totalOffset}px);"
            bind:this={wrapper}
        >
            {#each $guessedPokemonBlobs as guessedPokemonBlob}
                <Blob pokemonBlob={guessedPokemonBlob} />
            {/each}
        </div>
    </div>
</div>

<button on:click={() => addGuessBlob("butterfree")}>Add Butterfree</button>

<style scoped>
    #gradient-mask {
        /* Mask that makes the left edge transparent */
        mask: linear-gradient(
            to left,
            rgba(0, 0, 0, 1) 80%,
            rgba(0, 0, 0, 0) 100%
        );
        -webkit-mask: linear-gradient(
            to left,
            rgba(0, 0, 0, 1) 80%,
            rgba(0, 0, 0, 0) 100%
        );
    }
</style>
