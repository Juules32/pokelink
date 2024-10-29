<script >
    import { base } from "$app/paths";
    import TutorialComponent from "./TutorialComponent.svelte";
    const localFirstVisit = localStorage.getItem("firstVisit") ? false : true
    localStorage.setItem("firstVisit", "false")
    let showTutorial = $state(localFirstVisit);
</script>

<div class="z-50 h-16 sm:px-6 px-2 top-0 sticky bg-white flex items-center">
    <a href="{base}/" class="flex items-center">
        <img src="{base}/favicon.png" width="48px" alt="icon" />
        <p class="sm:visible text-2xl">PokéLink</p>
    </a>
    <div class="w-full flex justify-end sm:gap-x-4 gap-x-1">
        <a href="{base}/puzzles" class="rounded-lg px-2 text-2xl transition-colors hover:bg-gray-300">Puzzles</a>
        <div class="bg-gray-400 text-2xl w-[2px]"></div>
        <button class="rounded-lg px-2 text-2xl transition-colors hover:bg-gray-300" onclick={() => showTutorial = true}>Rules</button>
    </div>
</div>

<TutorialComponent bind:showTutorial />
