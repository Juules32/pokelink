<script lang="ts">
    import { browser } from "$app/environment";
    import { tick } from "svelte";
    import Blob from "./Blob.svelte";

    let guessedPokemonBlobs: number[] = [];
    let wrapper: HTMLElement;

    // Keeps track of the total shift in X
    let totalOffset = 0;

    if (browser) {
        // This should not use window width, but id = graphArea width
        totalOffset = window.innerWidth * 0.6;
    }

    async function addGuessBlob() {
        // Simply defines the new element as a number
        // This should be changed to some PokemonBlob interface
        guessedPokemonBlobs = [
            ...guessedPokemonBlobs,
            guessedPokemonBlobs.length + 1,
        ];

        await tick();

        const lastItem: HTMLElement | null = wrapper.querySelector(
            ".guessed-pokemon-blob:last-child"
        );
        if (lastItem) {
            const newOffsetAmount = lastItem.offsetWidth + 20;

            // Update the total offset to account for the new element's width
            totalOffset -= newOffsetAmount;

            // Set the opacity to completely visible
            // This triggers the opacity transition
            lastItem.style.opacity = "1";
        }
    }
</script>

<div
    id="graphArea"
    class="bg-red-400 w-3/4 p-4 h-[160px] rounded-lg border-black border-2"
>
    <div id="gradient-mask" class="relative overflow-hidden flex items-center">
        <div
            class="flex transition-transform duration-500"
            style="transform: translateX({totalOffset}px);"
            bind:this={wrapper}
        >
            {#each guessedPokemonBlobs as guessedPokemonBlob}
                <Blob data={guessedPokemonBlob} />
            {/each}
        </div>
    </div>
</div>

<button on:click={addGuessBlob}>Add Blob</button>

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
