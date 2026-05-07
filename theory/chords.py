from theory.scales import NOTES_FLAT, NOTES_SHARP, choose_note_system, get_note_index, spell_interval

MAJOR_CHORDS = ["", "m", "m", "", "", "m", "°"]
MINOR_CHORDS = ["m", "°", "", "m", "m", "", ""]

MAJOR_ROMAN = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
MINOR_ROMAN = ["i", "ii°", "III", "iv", "v", "VI", "VII"]


def build_chords(scale, chord_pattern):
    return [note + quality for note, quality in zip(scale, chord_pattern)]


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
