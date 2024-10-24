<script lang="ts">
    import { fetchHint } from "$lib/backend";
    import { edges, getPokemonNode, graphData, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import type { PokemonNode, Puzzle } from "$lib/interfaces";
    import NodeComponent from "./NodeComponent.svelte";
    import ArrowComponent from "./ArrowComponent.svelte";

    let guessedNodes: PokemonNode[] = [];
    let hint: string | undefined;
    let latestGuessNode: PokemonNode | undefined;

    export let date: string | undefined;
    export let puzzle: Puzzle;

    async function addHint() {
        if (latestGuessNode) {
            hint = await fetchHint(latestGuessNode.name, puzzle.target);
        }
    }

    function tryGuess(name: string) {
        if (latestGuessNode) {
            if (edges[latestGuessNode.name].includes(name)) {
                hint = undefined;
                addNode(name);
            }
        }
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
        latestGuessNode = guessedNodes.at(-1);
    }
</script>

<!-- 
    <button
        class="w-[128px] absolute left-0 text-center"
        on:click={() =>
        addNode(
            pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)].name
        )}
    >
        Add Random Pokemon
    </button>
-->

<div class="h-fit flex flex-col pt-12 space-y-5 items-center">
    <h1 class="text-5xl">{date ? "Puzzle: " + date : "Today's Puzzle"}</h1>
    <div class="flex items-center">
        <NodeComponent pokemonNode={getPokemonNode(puzzle.source)} />
        <ArrowComponent />
        <NodeComponent pokemonNode={getPokemonNode(puzzle.target)} />
    </div>

    <div class="flex w-full justify-center space-x-2">
        <div class="w-[80px]"></div>
        <SearchComponent {tryGuess} />
        <button
            on:click={addHint}
            class="bg-red-400 w-[80px] rounded-lg border-black border-2"
        >
            Hint?
        </button>
    </div>
    <GraphComponent graphNodes={guessedNodes} {hint} />

    {#if latestGuessNode?.name == puzzle.target}
        <h2 class="text-3xl">Shortest path</h2>
        <GraphComponent
            graphNodes={puzzle.shortestPath.map(
                (name) => graphData.nodes[name]
            )}
            hint={undefined}
        />
    {/if}
</div>
