<script lang="ts">
    import { fetchHint, fetchPuzzle } from "$lib/backend";
    import { getPokemonNode, graphData, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import NodeComponent from "./NodeComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import { page } from "$app/stores";
    import type { PokemonNode, Puzzle } from "$lib/interfaces";

    let date: string | null = $page.params.slug ? $page.params.slug : null;
    let guessedNodes: PokemonNode[] = []
    let hint: string;

    let puzzle: Puzzle;

    async function getHint() {
        const latestGuessNode = guessedNodes.at(-1)
        if (latestGuessNode)
            hint = await fetchHint(latestGuessNode.name, puzzle.target)
        console.log(graphData.nodes[hint])
    }

    export function addNode(guess: string) {
        const newNode = getPokemonNode(guess)
        guessedNodes = [...guessedNodes, newNode];
        if (puzzle.target == guess) {
            console.log("You win!")
        }
    }

    async function setupPuzzle() {
        const fetchedPuzzle = await fetchPuzzle(date);
        console.log("pee")
        puzzle = fetchedPuzzle
        if (!guessedNodes.length)
        addNode(puzzle.source);
    }
    
    setupPuzzle();
</script>
    
<div class="h-fit flex flex-col pt-32 space-y-10 items-center">
    <SearchComponent {guessedNodes} {addNode} />
    <GraphComponent graphNodes={guessedNodes} />
    
    <button on:click={() => addNode(pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)].name)}>Add Random Pokemon</button>
    
    <button on:click={getHint}>Get Hint</button>
    
    {#if hint}
        <NodeComponent pokemonNode={graphData.nodes[hint]} />
    {/if}
    
    {#if puzzle}
        <GraphComponent graphNodes={puzzle.shortestPath.map((name) => graphData.nodes[name])} />
    {/if}
</div>
