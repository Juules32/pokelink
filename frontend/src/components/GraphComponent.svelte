<script lang="ts">
    import NodeComponent from "./NodeComponent.svelte";
    import { afterUpdate } from "svelte";
    import type { PokemonNode } from "$lib/interfaces";
    import { graphData } from "$lib/state";
    import ArrowComponent from "./ArrowComponent.svelte";

    // Constants
    const gapSize = 20;

    export let hint: string | undefined;
    export let graphNodes: PokemonNode[];

    let scrollContainer: HTMLDivElement;
    afterUpdate(() => {
        if (scrollContainer) {
            scrollContainer.scrollTo({
                left: scrollContainer.scrollWidth,
                behavior: 'smooth'
            });
        }
    });
</script>

<div
    class="bg-red-400 w-3/4 min-h-[180px] h-[180px] rounded-lg border-black border-2"
>
    <div
        bind:this={scrollContainer}
        class="h-full flex items-center px-4 overflow-x-auto overflow-y-hidden whitespace-nowrap "
    >
        {#each graphNodes as guessedNode, i}
            {#if i}
                <ArrowComponent />
            {/if}
                <NodeComponent pokemonNode={guessedNode} />
        {/each}
        {#if hint}
            <ArrowComponent />
            <NodeComponent pokemonNode={graphData.nodes[hint]} isSecret={true} />
        {/if}
    </div>
</div>
