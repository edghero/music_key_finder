from theory.borrowed_chords import build_borrowed_chord_rows
from theory.chords import (
    MAJOR_CHORDS,
    MAJOR_ROMAN,
    MINOR_CHORDS,
    MINOR_ROMAN,
    build_chords,
    get_chord_root,
    get_dominant_for_target,
    get_secondary_dominants,
)
from theory.progressions import MAJOR_PROGRESSIONS, MINOR_PROGRESSIONS
from theory.scales import (
    MAJOR_PATTERN,
    MINOR_PATTERN,
    NOTES_FLAT,
    NOTES_SHARP,
    build_scale,
    choose_note_system,
    get_relative_key,
)
from theory.tritone_subs import get_tritone_substitution_for_target
from theory.utils import normalize_root


def ask_yes_no(prompt):
    choice = input(prompt).strip().lower()
    return choice in ["y", "yes"]


def get_mode_data(mode):
    if mode == "major":
        return MAJOR_PATTERN, MAJOR_CHORDS, MAJOR_ROMAN, MAJOR_PROGRESSIONS
    return MINOR_PATTERN, MINOR_CHORDS, MINOR_ROMAN, MINOR_PROGRESSIONS


def show_progressions(chords, mode):
    progressions = MAJOR_PROGRESSIONS if mode == "major" else MINOR_PROGRESSIONS

    print()
    print("Common chord progressions:")

    for key, (name, indexes) in progressions.items():
        progression_chords = [chords[i] for i in indexes]
        print(f"{key}. {name}: {' - '.join(progression_chords)}")


def show_tritone_substitutions(scale, root):
    notes_system = choose_note_system(root)

    print()
    print("Tritone substitutions:")

    for index, target in enumerate(scale):
        if index == 0:
            continue

        secondary_dominant = get_dominant_for_target(target, notes_system)
        tritone_sub = get_tritone_substitution_for_target(target, notes_system)
        print(f"SubV/{target}: {tritone_sub} instead of {secondary_dominant}")


def apply_tritone_substitutions_to_progressions(chords, mode, root):
    progressions = MAJOR_PROGRESSIONS if mode == "major" else MINOR_PROGRESSIONS
    notes_system = choose_note_system(root)

    print()
    print("Progressions with tritone substitutions:")

    for key, (name, indexes) in progressions.items():
        enhanced_progression = []

        for index, chord_index in enumerate(indexes):
            target_chord = chords[chord_index]
            target_root = get_chord_root(target_chord)

            if index != 0:
                tritone_sub = get_tritone_substitution_for_target(target_root, notes_system)
                enhanced_progression.append(tritone_sub)

            enhanced_progression.append(target_chord)

        print(f"{key}. {name}: {' - '.join(enhanced_progression)}")


def interactive_tonicization(chords, root):
    notes_system = choose_note_system(root)

    print()
    print("Choose a chord to tonicize:")

    for degree, chord in enumerate(chords[1:], start=2):
        print(f"{degree}. {chord}")

    choice = input("Enter a scale degree number: ").strip()

    if not choice.isdigit():
        print("Invalid choice.")
        return

    choice = int(choice)

    if choice < 2 or choice > len(chords):
        print("Invalid choice.")
        return

    target_chord = chords[choice - 1]
    target_root = get_chord_root(target_chord)

    secondary_dominant = get_dominant_for_target(target_root, notes_system)
    tritone_sub = get_tritone_substitution_for_target(target_root, notes_system)

    print()
    print(f"To tonicize {target_chord}, use: {secondary_dominant} -> {target_chord}")
    print(f"Tritone substitute: {tritone_sub} -> {target_chord}")


def show_borrowed_chords(root, chords):
    print()
    print("Borrowed chords / Modal interchange:")

    for row in build_borrowed_chord_rows(root, chords):
        print(f"{row['Mode']} {row['Roman']}: {row['Chord']}")


def main():
    print("Music Key Finder")
    print("----------------")

    root = normalize_root(input("Enter a root note, like C, D, F#, or Bb: "))
    mode = input("Enter major or minor: ").strip().lower()

    all_notes = NOTES_SHARP + NOTES_FLAT

    if root not in all_notes:
        print("Invalid root note. Try C, F#, Bb, Eb, etc.")
        return

    if mode not in ["major", "minor"]:
        print("Invalid mode. Please enter major or minor.")
        return

    pattern, chord_pattern, romans, _ = get_mode_data(mode)
    scale = build_scale(root, pattern)
    chords = build_chords(scale, chord_pattern)

    print()
    print(f"{root} {mode} scale:")
    print(" - ".join(scale))

    print()
    print("Diatonic chords:")
    for roman, chord in zip(romans, chords):
        print(f"{roman}: {chord}")

    notes_system = choose_note_system(root)
    secondary = get_secondary_dominants(scale, notes_system)

    print()
    print("Secondary dominants (V of):")
    for target, dominant in secondary.items():
        print(f"V/{target}: {dominant}7")

    show_tritone_substitutions(scale, root)

    relative = get_relative_key(scale, mode)
    print(f"Relative key: {relative}")

    show_progression_examples = ask_yes_no(
        "Would you like to see chord progression examples? (y/n): "
    )

    if show_progression_examples:
        show_progressions(chords, mode)
        apply_tritone_substitutions_to_progressions(chords, mode, root)

    wants_tonicization = ask_yes_no("Would you like to tonicize a chord? (y/n): ")

    if wants_tonicization:
        interactive_tonicization(chords, root)

    show_borrowed_chords(root, chords)


if __name__ == "__main__":
    main()
