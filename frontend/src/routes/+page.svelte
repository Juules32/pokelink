<script lang="ts">
    import { getRandomBackgroundPath } from "$lib/util";
    import Search from "$components/SearchArea.svelte";
    import Graph from "$components/GraphArea.svelte";
</script>

<div
    class="fixed inset-0 flex flex-col space-y-10 justify-center items-center bg-center bg-cover"
    style="background-image: url({getRandomBackgroundPath()});
		   image-rendering: pixelated;"
>
    <Search />
    <Graph />
</div>
