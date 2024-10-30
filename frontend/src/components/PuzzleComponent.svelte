<script lang="ts">
    import { fetchHint } from "$lib/backend";
    import { edges, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import type { Puzzle } from "$lib/interfaces";
    import NodeComponent from "./NodeComponent.svelte";
    import ArrowComponent from "./ArrowComponent.svelte";
    import { dev } from "$app/environment";
    import { confetti } from "@neoconfetti/svelte";

    interface Props {
        date: string | undefined;
        puzzle: Puzzle;
    }
    let { date, puzzle }: Props = $props();
    let guessedNames: string[] = $state([]);
    let hint: string | undefined = $state();
    const latestGuessName = $derived(guessedNames.at(-1));

    async function addHint() {
        if (latestGuessName) {
            hint = await fetchHint(latestGuessName, puzzle.target);
        }
    }

    function tryGuess(name: string) {
        if (latestGuessName) {
            if ($edges[latestGuessName].includes(name)) {
                addNode(name);
            }
        }
    }

    function addNode(guess: string) {
        hint = undefined;
        guessedNames = [...guessedNames, guess];
        if (puzzle.target == guess) {
            console.log("You win!");
        }
    }

    addNode(puzzle.source);

    let won = $derived(latestGuessName == puzzle.target);
    let numGuesses = $derived(guessedNames.length - 1)
</script>

{#if dev}
    <button
        class="w-[128px] absolute left-0 text-center"
        onclick={() => addNode(
            $pokemonNodes[Math.floor(Math.random() * $pokemonNodes.length)].name
        )}
    >
        Add Random Pokemon
    </button>
    <button
        class="w-[128px] absolute left-32 text-center"
        onclick={() => addNode(puzzle.target)}
    >
        Complete Puzzle
    </button>
{/if}

{#if won}
    <div
        style="position: absolute; left: 50%; top: 0%"
        use:confetti={{
            force: 0.7,
            stageWidth: window.innerWidth - 40, // 40 prevents overflow
            stageHeight: window.innerHeight - 16, // 16 prevents overflow
            colors: ["#ff3e00", "#40b3ff", "#676778"]
        }}
    ></div>
{/if}

<div class="h-fit flex flex-col pt-12 space-y-5 items-center">
    <h1 class="sm:text-5xl text-3xl">{date ? "Puzzle: " + date : "Today's Puzzle"}</h1>
    <div class="flex items-center">
        <NodeComponent pokemonName={puzzle.source} />
        <ArrowComponent />
        <NodeComponent pokemonName={puzzle.target} />
    </div>

    {#if won}
        <h2 class="sm:text-3xl text-xl">Your Solution: {numGuesses} {numGuesses > 1 ? "Guesses" : "Guess"}</h2>
    {:else}
        <div class="flex w-3/4 max-w-[500px] justify-center space-x-2">
            <SearchComponent {tryGuess} />
            <button
                onclick={addHint}
                class="bg-red-400 w-[80px] rounded-lg border-black border-2"
            >
                Hint?
            </button>
        </div>
    {/if}

    <GraphComponent 
        graphNames={guessedNames}
        {hint}
    />

    {#if won}
        <h2 class="sm:text-3xl text-xl">Shortest path: {puzzle.shortestPathLength} {puzzle.shortestPathLength > 1 ? "Guesses" : "Guess"}</h2>
        <GraphComponent
            graphNames={puzzle.shortestPath}
        />
    {/if}
</div>
