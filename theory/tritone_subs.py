from theory.scales import spell_interval


def get_tritone_substitution_for_target(target_root, notes_system=None):
    return spell_interval(target_root, semitones=1, letter_steps=1) + "7"
