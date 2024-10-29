<script lang="ts">
    import PuzzlesComponent from "$components/PuzzlesComponent.svelte";
    import type { PageData } from "./$types";

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();
</script>

<PuzzlesComponent puzzles={data.puzzles} />
