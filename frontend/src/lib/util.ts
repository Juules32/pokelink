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

export function isNameLegal(name: string) {
    return !(
        name.includes("rockruff-") ||
        name.includes("cramorant-") ||
        name.includes("greninja-") ||
        name.includes("-totem") ||
        (name.includes("zygarde-") && name != "zygarde-50") ||
        (name.includes("pikachu-") && name != "pikachu-gmax") ||
        (name.includes("eevee-") && name != "eevee-gmax")
    )
}
