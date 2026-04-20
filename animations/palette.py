from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    BG_0: str
    BG_1: str
    BG_2: str
    BG_3: str
    TEXT_PRIMARY: str
    TEXT_SECONDARY: str
    TEXT_MUTED: str
    TEXT_FAINT: str
    TEXT_INVERSE: str
    BORDER_SUBTLE: str
    BORDER: str
    BORDER_STRONG: str
    GRID_FAINT: str
    GRID: str
    AXIS: str
    BLUE: str
    CYAN: str
    TEAL: str
    GREEN: str
    LIME: str
    YELLOW: str
    AMBER: str
    ORANGE: str
    RED: str
    PINK: str
    PURPLE: str
    VIOLET: str
    BLUE_SOFT: str
    CYAN_SOFT: str
    TEAL_SOFT: str
    GREEN_SOFT: str
    LIME_SOFT: str
    YELLOW_SOFT: str
    AMBER_SOFT: str
    ORANGE_SOFT: str
    RED_SOFT: str
    PINK_SOFT: str
    PURPLE_SOFT: str
    VIOLET_SOFT: str
    INFO: str
    SUCCESS: str
    WARNING: str
    DANGER: str
    FOCUS: str
    EXAMPLE: str
    QUESTION: str
    ANSWER: str


PALETTES = {
    "Dark": Palette(
        BG_0="#0B0F14",
        BG_1="#111827",
        BG_2="#172033",
        BG_3="#1F2A3D",
        TEXT_PRIMARY="#E5EEF8",
        TEXT_SECONDARY="#B8C4D6",
        TEXT_MUTED="#8A97AB",
        TEXT_FAINT="#66758C",
        TEXT_INVERSE="#0B0F14",
        BORDER_SUBTLE="#263248",
        BORDER="#334155",
        BORDER_STRONG="#475569",
        GRID_FAINT="#1E293B",
        GRID="#273449",
        AXIS="#64748B",
        BLUE="#60A5FA",
        CYAN="#22D3EE",
        TEAL="#2DD4BF",
        GREEN="#4ADE80",
        LIME="#A3E635",
        YELLOW="#FACC15",
        AMBER="#F59E0B",
        ORANGE="#FB923C",
        RED="#F87171",
        PINK="#F472B6",
        PURPLE="#C084FC",
        VIOLET="#8B5CF6",
        BLUE_SOFT="#2C4A6B",
        CYAN_SOFT="#164E63",
        TEAL_SOFT="#134E4A",
        GREEN_SOFT="#1F4D35",
        LIME_SOFT="#3F5C1D",
        YELLOW_SOFT="#5A4A14",
        AMBER_SOFT="#643C12",
        ORANGE_SOFT="#6A3417",
        RED_SOFT="#5C2626",
        PINK_SOFT="#5B2743",
        PURPLE_SOFT="#4C2C63",
        VIOLET_SOFT="#3F2B63",
        INFO="#60A5FA",
        SUCCESS="#4ADE80",
        WARNING="#F59E0B",
        DANGER="#F87171",
        FOCUS="#22D3EE",
        EXAMPLE="#C084FC",
        QUESTION="#FACC15",
        ANSWER="#2DD4BF",
    ),
    "Light": Palette(
        BG_0="#F8FAFC",
        BG_1="#FFFFFF",
        BG_2="#EEF2F7",
        BG_3="#E2E8F0",
        TEXT_PRIMARY="#0F172A",
        TEXT_SECONDARY="#334155",
        TEXT_MUTED="#64748B",
        TEXT_FAINT="#94A3B8",
        TEXT_INVERSE="#F8FAFC",
        BORDER_SUBTLE="#CBD5E1",
        BORDER="#94A3B8",
        BORDER_STRONG="#64748B",
        GRID_FAINT="#E2E8F0",
        GRID="#CBD5E1",
        AXIS="#475569",
        BLUE="#2563EB",
        CYAN="#0891B2",
        TEAL="#0F766E",
        GREEN="#16A34A",
        LIME="#65A30D",
        YELLOW="#CA8A04",
        AMBER="#D97706",
        ORANGE="#EA580C",
        RED="#DC2626",
        PINK="#DB2777",
        PURPLE="#9333EA",
        VIOLET="#7C3AED",
        BLUE_SOFT="#DBEAFE",
        CYAN_SOFT="#CFFAFE",
        TEAL_SOFT="#CCFBF1",
        GREEN_SOFT="#DCFCE7",
        LIME_SOFT="#ECFCCB",
        YELLOW_SOFT="#FEF9C3",
        AMBER_SOFT="#FEF3C7",
        ORANGE_SOFT="#FFEDD5",
        RED_SOFT="#FEE2E2",
        PINK_SOFT="#FCE7F3",
        PURPLE_SOFT="#F3E8FF",
        VIOLET_SOFT="#EDE9FE",
        INFO="#2563EB",
        SUCCESS="#16A34A",
        WARNING="#D97706",
        DANGER="#DC2626",
        FOCUS="#0891B2",
        EXAMPLE="#9333EA",
        QUESTION="#CA8A04",
        ANSWER="#0F766E",
    ),
    "Sepia": Palette(
        BG_0="#F4ECD8",
        BG_1="#EFE4CC",
        BG_2="#E6D7BA",
        BG_3="#DCC8A5",
        TEXT_PRIMARY="#3E2F26",
        TEXT_SECONDARY="#5B4637",
        TEXT_MUTED="#7A6453",
        TEXT_FAINT="#A08A75",
        TEXT_INVERSE="#F4ECD8",
        BORDER_SUBTLE="#D6C2A3",
        BORDER="#BFA786",
        BORDER_STRONG="#9B8262",
        GRID_FAINT="#E5D7BF",
        GRID="#D3BE9E",
        AXIS="#7A6453",
        BLUE="#5B7FA3",
        CYAN="#4C8C8A",
        TEAL="#4F7A67",
        GREEN="#6E8B55",
        LIME="#8B9A4A",
        YELLOW="#C59A3D",
        AMBER="#B7792B",
        ORANGE="#B8643C",
        RED="#A8544A",
        PINK="#B06A7A",
        PURPLE="#84639C",
        VIOLET="#6D5B95",
        BLUE_SOFT="#D9E3EC",
        CYAN_SOFT="#D6E8E6",
        TEAL_SOFT="#D8E4DD",
        GREEN_SOFT="#DFE7D2",
        LIME_SOFT="#E8EACF",
        YELLOW_SOFT="#F0E3BA",
        AMBER_SOFT="#EAD7B3",
        ORANGE_SOFT="#E8CEBD",
        RED_SOFT="#E7C8C2",
        PINK_SOFT="#E7D0D7",
        PURPLE_SOFT="#DDD4E8",
        VIOLET_SOFT="#D7D3E6",
        INFO="#5B7FA3",
        SUCCESS="#6E8B55",
        WARNING="#B7792B",
        DANGER="#A8544A",
        FOCUS="#4C8C8A",
        EXAMPLE="#84639C",
        QUESTION="#C59A3D",
        ANSWER="#4F7A67",
    ),
}


def apply_palette(name: str) -> Palette:
    key = name.strip()
    if key not in PALETTES:
        raise ValueError(f"Unsupported COLOR_SCHEME: {name!r}")
    return PALETTES[key]
