from theory.chords import build_chords
from theory.scales import build_spelled_scale

MODAL_INTERCHANGE_MODES = {
    "Aeolian": {
        "pattern": [2, 1, 2, 2, 1, 2, 2],
        "chords": ["m", "°", "", "m", "m", "", ""],
        "romans": ["i", "ii°", "bIII", "iv", "v", "bVI", "bVII"],
    },
    "Harmonic Minor": {
        "pattern": [2, 1, 2, 2, 1, 3, 1],
        "chords": ["m", "°", "+", "m", "", "", "°"],
        "romans": ["i", "ii°", "bIII+", "iv", "V", "bVI", "vii°"],
    },
    "Melodic Minor": {
        "pattern": [2, 1, 2, 2, 2, 2, 1],
        "chords": ["m", "m", "+", "", "", "°", "°"],
        "romans": ["i", "ii", "bIII+", "IV", "V", "vi°", "vii°"],
    },
    "Dorian": {
        "pattern": [2, 1, 2, 2, 2, 1, 2],
        "chords": ["m", "m", "", "", "m", "°", ""],
        "romans": ["i", "ii", "bIII", "IV", "v", "vi°", "bVII"],
    },
    "Phrygian": {
        "pattern": [1, 2, 2, 2, 1, 2, 2],
        "chords": ["m", "", "", "m", "°", "", "m"],
        "romans": ["i", "bII", "bIII", "iv", "v°", "bVI", "bvii"],
    },
    "Lydian": {
        "pattern": [2, 2, 2, 1, 2, 2, 1],
        "chords": ["", "", "m", "°", "", "m", "m"],
        "romans": ["I", "II", "iii", "#iv°", "V", "vi", "vii"],
    },
    "Mixolydian": {
        "pattern": [2, 2, 1, 2, 2, 1, 2],
        "chords": ["", "m", "°", "", "m", "m", ""],
        "romans": ["I", "ii", "iii°", "IV", "v", "vi", "bVII"],
    },
}


def build_modal_interchange_rows(root):
    rows = []

    for mode_name, mode_data in MODAL_INTERCHANGE_MODES.items():
        modal_scale = build_spelled_scale(root, mode_data["pattern"])
        modal_chords = build_chords(modal_scale, mode_data["chords"])

        rows.append(
            {
                "Mode": mode_name,
                "Notes": " - ".join(modal_scale),
                "Chords": " - ".join(modal_chords),
            }
        )

    return rows


def build_borrowed_chord_rows(root, home_chords):
    home_chord_set = set(home_chords)
    rows = []
    seen = set()

    for mode_name, mode_data in MODAL_INTERCHANGE_MODES.items():
        modal_scale = build_spelled_scale(root, mode_data["pattern"])
        modal_chords = build_chords(modal_scale, mode_data["chords"])

        for roman, scale_tone, chord in zip(mode_data["romans"], modal_scale, modal_chords):
            if chord in home_chord_set or chord in seen:
                continue

            seen.add(chord)
            rows.append(
                {
                    "Mode": mode_name,
                    "Roman": roman,
                    "Scale Tone": scale_tone,
                    "Chord": chord,
                }
            )

    return rows
