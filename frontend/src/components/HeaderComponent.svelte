<script >
    import { base } from "$app/paths";
    import TutorialComponent from "./TutorialComponent.svelte";
    const localFirstVisit = localStorage.getItem("firstVisit") ? false : true
    localStorage.setItem("firstVisit", "false")
    let showTutorial = $state(localFirstVisit);
</script>

<div class="z-50 h-16 px-8 top-0 sticky bg-white flex items-center">
    <a href="{base}/" class="flex items-center">
        <img src="{base}/favicon.png" width="48px" alt="icon" />
        <p class="text-3xl">PokéLink</p>
    </a>
    <div class="w-full flex justify-end gap-x-10 px-8">
        <p class="text-2xl">Puzzles</p>
        <button class="text-2xl" onclick={() => showTutorial = true}>Rules</button>
    </div>
</div>

<TutorialComponent bind:showTutorial />
