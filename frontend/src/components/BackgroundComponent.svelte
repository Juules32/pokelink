<script lang="ts">
    import { base } from "$app/paths";
    
    function getRandomBackgroundPath() {
        const backgroundNames: string[] = [
            "forest",
            "berry-forest",
            "cave",
            "cave2",
            "cave3",
            "cave4",
            "chamber",
            "hideout",
            "mansion",
            "mt-ember",
            "power-plant",
            "safari",
            "tower",
            "tower2",
            "victory-road",
            "warehouse"
        ];
        return `${base}/backgrounds/${backgroundNames[Math.floor(Math.random() * backgroundNames.length)]}.png`;
    }
</script>

<div
    class="-z-10 fixed w-screen h-screen bg-center bg-cover"
    style="background-image: url({getRandomBackgroundPath()});
           image-rendering: pixelated;"
></div>
