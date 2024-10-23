<script>
    import { page } from "$app/stores";
</script>

<div class="h-40 flex flex-col justify-center items-center">
    <h1 class="text-7xl">{$page.status}</h1>
    <h1 class="text-3xl">{$page.error?.message}</h1>
    <a class="text-2xl underline text-blue-500" href="/">Go back to the home page</a>
</div>
