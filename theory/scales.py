NOTES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

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


def get_relative_key(scale, mode):
    if mode == "major":
        relative_root = scale[5]
        return f"{relative_root} minor"

    relative_root = scale[2]
    return f"{relative_root} major"
