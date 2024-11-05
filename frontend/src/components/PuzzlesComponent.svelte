<script lang="ts">
    import { goto, preloadData } from "$app/navigation";
    import { base } from "$app/paths";
    import type { PuzzlesItem } from "$lib/interfaces";
    import ArrowComponent from "./ArrowComponent.svelte";
    import NodeComponent from "./NodeComponent.svelte";
    import PuzzleLinksComponent from "./PuzzleLinksComponent.svelte";

    interface Props {
        puzzles: PuzzlesItem[];
        numPuzzles: number;
        pageNum: number;
    }
    let { puzzles, numPuzzles, pageNum }: Props = $props();

    let innerWidth: number | undefined = $state();

    const showSmallTable = $derived(innerWidth ? innerWidth < 750 : false);

</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col items-center py-12">
    <div class="bg-red-400 p-5 border-2 border-black rounded-lg">
        {#if showSmallTable}
            <h1 class="text-center text-3xl pb-4">Previous Puzzles</h1>
        {:else}
            <h1 class="text-center text-5xl pb-4">Previous Puzzles</h1>
        {/if}
        
        <div class="flex justify-center pb-2">
            <PuzzleLinksComponent {pageNum} {numPuzzles} />
        </div>
        <table class="bg-white border-2 border-black rounded-lg">
            <thead class="text-xl">
                <tr>
                    {#if showSmallTable}
                        <th>Date</th>
                        <th>Status</th>
                    {:else}
                        <th>Date</th>
                        <th>From</th>
                        <th></th>
                        <th>To</th>
                        <th>Status</th>
                    {/if}
                </tr>
            </thead>
            <tbody class="divide-y-2 divide-dashed">
                {#each puzzles as puzzle}
                    <!-- svelte-ignore a11y_mouse_events_have_key_events -->
                    <tr class="puzzle-item space-y-10" onmouseover={async () => {await preloadData(`${base}/puzzles/${puzzle.date}`)}} onclick={() => goto(`${base}/puzzles/${puzzle.date}`)}>
                        {#if showSmallTable}
                            <td>{puzzle.date}</td>
                            <td>{puzzle.completed ? "Completed" : "Not Completed"}</td>
                        {:else}
                            <td>{puzzle.date}</td>
                            <td> <NodeComponent pokemonName={puzzle.source} /> </td>
                            <td> <ArrowComponent /> </td>
                            <td> <NodeComponent pokemonName={puzzle.target} /> </td>
                            <td class="text-center w-0">{puzzle.completed ? "Completed" : "Not Completed"}</td>
                        {/if}
                    </tr>
                {/each}
            </tbody>
        </table>
        <div class="flex justify-center pt-2">
            <PuzzleLinksComponent {pageNum} {numPuzzles} />
        </div>
    </div>
</div>

<style scoped>
    .puzzle-item {
        cursor: pointer;
    }

    th, td {
        padding: 10px 20px;
    }
</style>
