<script>
    export let data;
</script>

<div class="bg-white mx-[10px] p-[10px] h-[128px] w-[128px] opacity-0 rounded-full text-center whitespace-nowrap transition-opacity duration-500 bg-center bg-no-repeat guessed-pokemon-blob">{data}</div>

<style scoped>
    .guessed-pokemon-blob {
        background-image: url("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/904.png");
    }
</style>
