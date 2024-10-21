export function getRandomBackgroundPath() {
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
        "warehouse",
    ];
    return `backgrounds/${backgroundNames[Math.floor(Math.random() * backgroundNames.length)]}.png`;
}

export function getSpriteUrl(id: number): string {
    return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${id}.png`
}
