from theory.scales import NOTES_FLAT, NOTES_SHARP, choose_note_system, get_note_index, spell_interval

MAJOR_CHORDS = ["", "m", "m", "", "", "m", "°"]
MINOR_CHORDS = ["m", "°", "", "m", "m", "", ""]

MAJOR_ROMAN = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
MINOR_ROMAN = ["i", "ii°", "III", "iv", "v", "VI", "VII"]

CHORD_QUALITIES = {
    "Major": {
        "symbol": "",
        "intervals": [(0, 0, "Root"), (4, 2, "Major 3rd"), (7, 4, "Perfect 5th")],
        "default_seventh": (11, 6, "Major 7th", "maj7"),
    },
    "Minor": {
        "symbol": "m",
        "intervals": [(0, 0, "Root"), (3, 2, "Minor 3rd"), (7, 4, "Perfect 5th")],
        "default_seventh": (10, 6, "Minor 7th", "7"),
    },
    "Dominant": {
        "symbol": "7",
        "intervals": [(0, 0, "Root"), (4, 2, "Major 3rd"), (7, 4, "Perfect 5th")],
        "default_seventh": (10, 6, "Minor 7th", "7"),
    },
    "Diminished": {
        "symbol": "°",
        "intervals": [(0, 0, "Root"), (3, 2, "Minor 3rd"), (6, 4, "Diminished 5th")],
        "default_seventh": (9, 6, "Diminished 7th", "7"),
    },
    "Augmented": {
        "symbol": "+",
        "intervals": [(0, 0, "Root"), (4, 2, "Major 3rd"), (8, 4, "Augmented 5th")],
        "default_seventh": (10, 6, "Minor 7th", "7"),
    },
    "Sus2": {
        "symbol": "sus2",
        "intervals": [(0, 0, "Root"), (2, 1, "Major 2nd"), (7, 4, "Perfect 5th")],
        "default_seventh": (10, 6, "Minor 7th", "7"),
    },
    "Sus4": {
        "symbol": "sus4",
        "intervals": [(0, 0, "Root"), (5, 3, "Perfect 4th"), (7, 4, "Perfect 5th")],
        "default_seventh": (10, 6, "Minor 7th", "7"),
    },
}

CHORD_EXTENSIONS = {
    "Triad": {"symbol": "", "intervals": []},
    "6th": {"symbol": "6", "intervals": [(9, 5, "Major 6th")]},
    "add9": {"symbol": "add9", "intervals": [(14, 1, "Major 9th")]},
    "add11": {"symbol": "add11", "intervals": [(17, 3, "Perfect 11th")]},
    "add13": {"symbol": "add13", "intervals": [(21, 5, "Major 13th")]},
    "7th": {"symbol": None, "intervals": ["default_seventh"]},
    "Major 7th": {"symbol": "maj7", "intervals": [(11, 6, "Major 7th")]},
    "9th": {"symbol": "9", "intervals": ["default_seventh", (14, 1, "Major 9th")]},
    "11th": {
        "symbol": "11",
        "intervals": ["default_seventh", (14, 1, "Major 9th"), (17, 3, "Perfect 11th")],
    },
    "13th": {
        "symbol": "13",
        "intervals": [
            "default_seventh",
            (14, 1, "Major 9th"),
            (17, 3, "Perfect 11th"),
            (21, 5, "Major 13th"),
        ],
    },
    "b9": {"symbol": "7b9", "intervals": ["default_seventh", (13, 1, "Flat 9th")]},
    "#9": {"symbol": "7#9", "intervals": ["default_seventh", (15, 1, "Sharp 9th")]},
    "#11": {"symbol": "7#11", "intervals": ["default_seventh", (18, 3, "Sharp 11th")]},
    "b13": {"symbol": "7b13", "intervals": ["default_seventh", (20, 5, "Flat 13th")]},
}


def build_chords(scale, chord_pattern):
    return [note + quality for note, quality in zip(scale, chord_pattern)]


def get_chord_quality_names():
    return list(CHORD_QUALITIES.keys())


def get_chord_extension_names():
    return list(CHORD_EXTENSIONS.keys())


def build_chord_finder_result(root, quality_name, extension_name):
    quality = CHORD_QUALITIES[quality_name]
    extension = CHORD_EXTENSIONS[extension_name]
    interval_specs = quality["intervals"].copy()

    if quality_name == "Dominant" and extension_name == "Triad":
        interval_specs.append(quality["default_seventh"])

    for interval in extension["intervals"]:
        if interval == "default_seventh":
            default_seventh = quality["default_seventh"]
            if default_seventh not in interval_specs:
                interval_specs.append(default_seventh)
        else:
            interval_specs.append(interval)

    tones = []
    rows = []
    seen_note_indexes = set()

    for interval_spec in interval_specs:
        semitones, letter_steps, interval_name = interval_spec[:3]
        note = spell_interval(root, semitones, letter_steps)
        note_index = get_note_index(note)

        if note_index in seen_note_indexes:
            continue

        seen_note_indexes.add(note_index)
        tones.append(note)
        rows.append(
            {
                "Tone": note,
                "Interval": interval_name,
            }
        )

    if quality_name == "Dominant" and extension_name == "Triad":
        extension_symbol = "7"
    elif extension["symbol"] is None:
        extension_symbol = quality["default_seventh"][3]
    elif quality_name == "Major" and extension_name in ["9th", "11th", "13th"]:
        extension_symbol = "maj" + extension["symbol"]
    elif quality_name == "Major" and extension_name in ["b9", "#9", "#11", "b13"]:
        extension_symbol = "maj" + extension["symbol"]
    else:
        extension_symbol = extension["symbol"]

    quality_symbol = "" if quality_name == "Dominant" and extension_symbol else quality["symbol"]
    symbol = f"{root}{quality_symbol}{extension_symbol}"

    return {
        "symbol": symbol,
        "tones": tones,
        "rows": rows,
    }


def build_triad_tones(scale, chord_index):
    return [
        scale[chord_index % len(scale)],
        scale[(chord_index + 2) % len(scale)],
        scale[(chord_index + 4) % len(scale)],
    ]


def get_chord_root(chord):
    return chord.replace("m", "").replace("°", "").replace("7", "").replace("+", "")


def get_dominant_for_target(target_root, notes_system=None):
    return spell_interval(target_root, semitones=7, letter_steps=4) + "7"


def get_secondary_dominants(scale, notes_system):
    secondary_dominants = {}

    for index, target in enumerate(scale):
        if index == 0:
            continue

        dominant = get_dominant_for_target(target, notes_system).replace("7", "")
        secondary_dominants[target] = dominant

    return secondary_dominants


def get_note_distance(root, note):
    return (get_note_index(note) - get_note_index(root)) % 12


def get_extended_chord_symbol(root, triad_quality, seventh_note, extension):
    seventh_distance = get_note_distance(root, seventh_note)

    if triad_quality == "":
        seventh_quality = "maj" if seventh_distance == 11 else ""
        return f"{root}{seventh_quality}{extension}"

    if triad_quality == "m":
        return f"{root}m{extension}"

    if triad_quality == "°":
        if extension == "7":
            return f"{root}m7b5"
        return f"{root}m7b5 add{extension}"

    return f"{root}{triad_quality}{extension}"


def build_extended_chord_rows(romans, scale, chord_pattern):
    rows = []

    for index, (roman, root, triad_quality) in enumerate(zip(romans, scale, chord_pattern)):
        third = scale[(index + 2) % len(scale)]
        fifth = scale[(index + 4) % len(scale)]
        seventh = scale[(index + 6) % len(scale)]
        ninth = scale[(index + 1) % len(scale)]
        eleventh = scale[(index + 3) % len(scale)]
        thirteenth = scale[(index + 5) % len(scale)]

        rows.append(
            {
                "Roman": roman,
                "Base Chord": root + triad_quality,
                "7th": f"{get_extended_chord_symbol(root, triad_quality, seventh, '7')} ({seventh})",
                "9th": f"{get_extended_chord_symbol(root, triad_quality, seventh, '9')} ({ninth})",
                "11th": f"{get_extended_chord_symbol(root, triad_quality, seventh, '11')} ({eleventh})",
                "13th": f"{get_extended_chord_symbol(root, triad_quality, seventh, '13')} ({thirteenth})",
                "Chord Tones": " - ".join([root, third, fifth, seventh, ninth, eleventh, thirteenth]),
            }
        )

    return rows


def build_altered_dominant_rows(root):
    notes_system = choose_note_system(root)
    root_index = notes_system.index(root)
    dominant_root = notes_system[(root_index + 7) % len(notes_system)]
    dominant_index = NOTES_SHARP.index(dominant_root) if dominant_root in NOTES_SHARP else NOTES_FLAT.index(dominant_root)

    altered_tones = {
        "b9": NOTES_FLAT[(dominant_index + 1) % len(NOTES_FLAT)],
        "#9": NOTES_SHARP[(dominant_index + 3) % len(NOTES_SHARP)],
        "#11": NOTES_SHARP[(dominant_index + 6) % len(NOTES_SHARP)],
        "b13": NOTES_FLAT[(dominant_index + 8) % len(NOTES_FLAT)],
    }

    return [
        {
            "Chord": dominant_root + "7",
            "Alteration": alteration,
            "Color Tone": tone,
            "Symbol": f"{dominant_root}7{alteration}",
        }
        for alteration, tone in altered_tones.items()
    ]
