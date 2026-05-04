from theory.chords import get_chord_root, get_dominant_for_target
from theory.scales import choose_note_system
from theory.tritone_subs import get_tritone_substitution_for_target

MAJOR_PROGRESSIONS = {
    "1": ("I-V-vi-IV", [0, 4, 5, 3]),
    "2": ("ii-V-I", [1, 4, 0]),
    "3": ("I-vi-IV-V", [0, 5, 3, 4]),
}

MINOR_PROGRESSIONS = {
    "1": ("i-VI-III-VII", [0, 5, 2, 6]),
    "2": ("i-iv-v", [0, 3, 4]),
    "3": ("i-VII-VI-VII", [0, 6, 5, 6]),
}


def build_progression_rows(progressions, chords, root):
    notes_system = choose_note_system(root)
    rows = []

    for _, (name, indexes) in progressions.items():
        progression_chords = [chords[i] for i in indexes]
        secondary_version = []
        tritone_version = []

        for position, chord in enumerate(progression_chords):
            target_root = get_chord_root(chord)

            if position != 0:
                secondary_version.append(get_dominant_for_target(target_root, notes_system))
                tritone_version.append(get_tritone_substitution_for_target(target_root, notes_system))

            secondary_version.append(chord)
            tritone_version.append(chord)

        rows.append(
            {
                "Progression": name,
                "Chords": " - ".join(progression_chords),
                "With Secondary Dominants": " - ".join(secondary_version),
                "With Tritone Subs": " - ".join(tritone_version),
            }
        )

    return rows
