<script lang="ts">
    import Search from "$components/Search.svelte";
    import { getRandomBackgroundPath } from "$lib/util";
</script>

<div
    class="fixed inset-0 flex flex-col justify-center items-center bg-center bg-cover"
    style="background-image: url({getRandomBackgroundPath()});
		   image-rendering: pixelated;"
>
    <Search />
</div>
