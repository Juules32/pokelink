<script lang="ts">
    import PuzzleComponent from "$components/PuzzleComponent.svelte";
    import type { PageData } from "./$types";

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();
</script>

<PuzzleComponent puzzle={data.puzzle} date={data.date}/>
