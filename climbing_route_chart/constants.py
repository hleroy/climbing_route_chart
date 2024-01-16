# Font sizes
TITLE_FS = 14
GRADE_FS = 18
SETTER_FS = 8

# Disk radius in mm
RADIUS = 69.5

# Hex code to color mapping
HEX_TO_COLOR_MAPPING = {
    "#ff0000": ["ROUGE", "RED"],
    "#ffff00": ["JAUNE", "YELLOW"],
    "#008200": ["VERT", "VERTE", "GREEN"],
    "#0000ff": ["BLEU", "BLEUE", "BLUE"],
    "#ffffff": ["BLANC", "BLANCHE", "WHITE"],
    "#000000": ["NOIR", "NOIRE", "BLACK"],
    "#a52829": ["BRUN", "BRUNE", "BROWN"],
    "#ffa600": ["ORANGE", "ORANGE"],
    "#ff9e1c": ["ORANGE FLUO", "FLUO ORANGE"],
    "#018651": ["VERT FLUO", "VERTE FLUO", "FLUO GREEN"],
    "#f0ff21": ["JAUNE FLUO", "JAUNE FLUO", "FLUO YELLOW"],
    "#ff3fc3": ["ROSE FLUO", "ROSE FLUO", "FLUO PINK"],
    "#b24499": ["VIOLET FLUO", "VIOLETTE FLUO", "FLUO VIOLET"],
    "#848284": ["GRIS", "GRISE", "GREY"],
    "#852475": ["VIOLET", "VIOLETTE", "PURPLE"],
    "#77bbbd": ["MENTHE", "MINT"],
    "#e0b0ff": ["MAUVE", "MAUVE"],
    "#FFC0CB": ["ROSE", "PINK"],
    # Add more colors as needed
}

# Inverting HEX_TO_COLOR_MAPPING to COLOR_MAPPING
COLOR_MAPPING = {}
for hex_code, names in HEX_TO_COLOR_MAPPING.items():
    for name in names:
        COLOR_MAPPING[name] = hex_code
