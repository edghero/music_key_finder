from theory.scales import NOTES_FLAT


def get_tritone_substitution_for_target(target_root, notes_system):
    target_index = notes_system.index(target_root)
    tritone_sub_index = (target_index + 1) % len(notes_system)
    return NOTES_FLAT[tritone_sub_index] + "7"
