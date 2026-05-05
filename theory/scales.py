NOTES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
NATURAL_NOTE_INDEX = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NOTE_LETTERS = ["C", "D", "E", "F", "G", "A", "B"]

MAJOR_PATTERN = [2, 2, 1, 2, 2, 2, 1]
MINOR_PATTERN = [2, 1, 2, 2, 1, 2, 2]


def choose_note_system(root):
    flat_keys = ["F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]

    if "b" in root or root in flat_keys:
        return NOTES_FLAT
    return NOTES_SHARP


def choose_modal_note_system(root, mode_name):
    if "#" in root:
        return NOTES_SHARP

    if "b" in root:
        return NOTES_FLAT

    if mode_name == "Lydian":
        return NOTES_SHARP

    return NOTES_FLAT


def build_scale(root, pattern):
    notes = choose_note_system(root)
    return build_scale_with_notes(root, pattern, notes)


def build_scale_with_notes(root, pattern, notes):
    scale = [root]
    index = notes.index(root)

    for step in pattern[:-1]:
        index = (index + step) % len(notes)
        scale.append(notes[index])

    return scale


def get_note_index(note):
    letter = note[0].upper()
    index = NATURAL_NOTE_INDEX[letter]

    for accidental in note[1:]:
        if accidental == "#":
            index += 1
        elif accidental == "b":
            index -= 1

    return index % 12


def spell_note(letter, note_index):
    natural_index = NATURAL_NOTE_INDEX[letter]
    distance = (note_index - natural_index) % 12

    if distance == 0:
        return letter
    if distance == 1:
        return letter + "#"
    if distance == 2:
        return letter + "##"
    if distance == 11:
        return letter + "b"
    if distance == 10:
        return letter + "bb"

    return NOTES_SHARP[note_index]


def build_spelled_scale(root, pattern):
    root_letter = root[0].upper()
    letter_index = NOTE_LETTERS.index(root_letter)
    note_index = get_note_index(root)
    scale = [root]

    for degree, step in enumerate(pattern[:-1], start=1):
        note_index = (note_index + step) % 12
        letter = NOTE_LETTERS[(letter_index + degree) % len(NOTE_LETTERS)]
        scale.append(spell_note(letter, note_index))

    return scale


def get_relative_key(scale, mode):
    if mode == "major":
        relative_root = scale[5]
        return f"{relative_root} minor"

    relative_root = scale[2]
    return f"{relative_root} major"
