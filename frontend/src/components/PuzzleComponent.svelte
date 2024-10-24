<script lang="ts">
    import { fetchHint, fetchPuzzle } from "$lib/backend";
    import { getPokemonNode, graphData, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import NodeComponent from "./NodeComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import type { PokemonNode, Puzzle } from "$lib/interfaces";

    let guessedNodes: PokemonNode[] = [];
    let hint: string | undefined;

    export let puzzle: Puzzle;

    async function getHint() {
        const latestGuessNode = guessedNodes.at(-1);
        if (latestGuessNode)
            hint = await fetchHint(latestGuessNode.name, puzzle.target);
    }

    export function addNode(guess: string) {
        const newNode = getPokemonNode(guess);
        guessedNodes = [...guessedNodes, newNode];
        if (puzzle.target == guess) {
            console.log("You win!");
        }
    }
    if (!guessedNodes.length) addNode(puzzle.source);

    $: {
        console.log("pee")
        hint = undefined
    }
</script>

<div class="w-[128px] h-2 absolute right-0 text-center">
    {#if hint}
        <NodeComponent pokemonNode={graphData.nodes[hint]} isSecret={true} />
    {:else}
        <button on:click={getHint} class="">Get Hint</button>
    {/if}
</div>
<div class="h-fit flex flex-col pt-32 space-y-10 items-center">
    <SearchComponent {guessedNodes} {addNode} />
    <GraphComponent graphNodes={guessedNodes} />

    <button
        on:click={() =>
            addNode(
                pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)]
                    .name
            )}>Add Random Pokemon</button
    >

    {#if puzzle}
        <GraphComponent
            graphNodes={puzzle.shortestPath.map(
                (name) => graphData.nodes[name]
            )}
        />
    {/if}
</div>
