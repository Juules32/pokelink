<script lang="ts">
    import { getRandomBackgroundPath } from "$lib/util";
</script>

<div
    class="-z-10 fixed w-screen h-screen bg-center bg-cover"
    style="background-image: url({getRandomBackgroundPath()});
           image-rendering: pixelated;"
></div>
