<script lang="ts">
    import { getRandomBackgroundPath } from "$lib/util";
    import SearchComponent from "$components/SearchComponent.svelte";
    import GraphComponent from "$components/GraphComponent.svelte";
    import { onMount } from "svelte";
    import PuzzleComponent from "$components/PuzzleComponent.svelte";

    let loaded = false;
    onMount(() => {
        loaded = true;
    });
</script>

{#if loaded}
    <div
        class="fixed inset-0 bg-center bg-cover"
        style="background-image: url({getRandomBackgroundPath()});
		   image-rendering: pixelated;"
    >
        <PuzzleComponent />
    </div>
{/if}
