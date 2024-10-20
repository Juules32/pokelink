<script lang="ts">
    import { getRandomBackgroundPath } from "$lib/util";
    import SearchComponent from "$components/SearchComponent.svelte";
    import GraphComponent from "$components/GraphComponent.svelte";
    import { onMount } from "svelte";

    let loaded = false;
    onMount(() => {
        loaded = true;
    });
</script>

{#if loaded}
    <div
        class="fixed inset-0 flex flex-col space-y-10 justify-center items-center bg-center bg-cover"
        style="background-image: url({getRandomBackgroundPath()});
		   image-rendering: pixelated;"
    >
        <SearchComponent />
        <GraphComponent />
    </div>
{/if}
