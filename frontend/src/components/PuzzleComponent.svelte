<script lang="ts">
    import { fetchHint, fetchPuzzle } from "$lib/backend";
    import { addNode, graphData, guessedNodes, pokemonNodes, puzzle } from "$lib/state";
    import { onMount } from "svelte";
    import GraphComponent from "./GraphComponent.svelte";
    import NodeComponent from "./NodeComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";

    let hint: string;
    async function getHint() {
        const latestGuessNode = $guessedNodes.at(-1)
        if (latestGuessNode)
            hint = await fetchHint(latestGuessNode.name, $puzzle.target)
        console.log(graphData.nodes[hint])
    }

    async function setupPuzzle() {
        $puzzle = await fetchPuzzle();
        if (!$guessedNodes.length)
            addNode($puzzle.source);
    }

    onMount(() => {
        setupPuzzle();
    });

</script>

<div class="h-fit flex flex-col pt-32 space-y-10 items-center">
    <SearchComponent />
    <GraphComponent graphNodes={$guessedNodes} />

    <!-- Debugging Button -->
    <button on:click={() => addNode(pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)].name)}>Add Random Pokemon</button>

    <button on:click={getHint}>Get Hint</button>

    {#if hint}
        <NodeComponent pokemonNode={graphData.nodes[hint]} />
    {/if}

    {#if $puzzle}
        <GraphComponent graphNodes={$puzzle.shortestPath.map((name) => graphData.nodes[name])} />
    {/if}
</div>
