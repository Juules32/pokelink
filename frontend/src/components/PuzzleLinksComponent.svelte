<script lang="ts">
    import { base } from "$app/paths";

    interface Props {
        pageNum: number;
        numPuzzles: number;
    }
    let { pageNum, numPuzzles }: Props = $props();

    function determinePageLinks(pageNum: number, numPuzzles: number): number[] {
        const numPageLinks = Math.ceil(numPuzzles / 10);
        const maxPageLinks = Math.min(numPageLinks, 5);
        if (pageNum == 1 || pageNum == 2) {
            return Array.from({ length: maxPageLinks }, (_, i) => 1 + i);
        }
        if (pageNum == numPageLinks || pageNum == numPageLinks - 1) {
            return Array.from({ length: maxPageLinks }, (_, i) => numPageLinks - maxPageLinks + 1 + i);
        }
        return Array.from({ length: maxPageLinks }, (_, i) => pageNum - 2 + i);
    }

    const pageLinks = $derived(determinePageLinks(pageNum, numPuzzles));
</script>

<div class="bg-white border-2 border-black rounded-lg p-2 space-x-2">
    {#each pageLinks as pageLink}
        <a
            style="background-color: {pageNum == pageLink ? 'rgb(248,113,113)' : ''}"
            href="{base}/puzzles?page={pageLink}"
            class="px-2 py-1 rounded-lg transition-colors hover:bg-gray-300"
        >
            {pageLink}
        </a>
    {/each}
</div>
