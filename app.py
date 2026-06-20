import streamlit as st
import streamlit.components.v1 as components

from instruments.guitar import render_fretboard_html
from instruments.piano import render_keyboard_html
from theory.borrowed_chords import build_borrowed_chord_rows, build_modal_interchange_rows
from theory.chords import (
    MAJOR_CHORDS,
    MAJOR_ROMAN,
    MINOR_CHORDS,
    MINOR_ROMAN,
    build_altered_dominant_rows,
    build_chord_finder_result,
    build_chords,
    build_extended_chord_rows,
    get_chord_extension_names,
    get_chord_quality_names,
    get_chord_root,
    get_dominant_for_target,
    get_secondary_dominants,
)
from theory.progressions import MAJOR_PROGRESSIONS, MINOR_PROGRESSIONS, build_progression_rows
from theory.scales import (
    MAJOR_PATTERN,
    MINOR_PATTERN,
    build_scale,
    choose_note_system,
    get_relative_key,
)
from theory.tritone_subs import get_tritone_substitution_for_target
from theory.utils import format_sequence

ROOT_OPTIONS = [
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
]


def get_mode_data(mode):
    if mode == "major":
        return MAJOR_PATTERN, MAJOR_CHORDS, MAJOR_ROMAN, MAJOR_PROGRESSIONS
    return MINOR_PATTERN, MINOR_CHORDS, MINOR_ROMAN, MINOR_PROGRESSIONS


def build_diatonic_chord_rows(romans, scale, chords):
    rows = []

    for roman, note, chord in zip(romans, scale, chords):
        rows.append(
            {
                "Roman": roman,
                "Scale Tone": note,
                "Chord": chord,
            }
        )

    return rows


def build_secondary_dominant_rows(scale, root):
    notes_system = choose_note_system(root)
    secondary_dominants = get_secondary_dominants(scale, notes_system)
    rows = []

    for target, dominant in secondary_dominants.items():
        rows.append(
            {
                "Target": target,
                "Secondary Dominant": f"{dominant}7",
                "Tritone Substitute": get_tritone_substitution_for_target(target, notes_system),
            }
        )

    return rows


def show_key_summary(root, mode, scale, chords, relative_key):
    st.subheader(f"{root} {mode}")

    scale_col, relative_col, chord_col = st.columns(3)
    with scale_col:
        st.metric("Scale tones", len(scale))
    with relative_col:
        st.metric("Relative key", relative_key)
    with chord_col:
        st.metric("Diatonic chords", len(chords))

    st.info(format_sequence(scale))


def main():
    st.set_page_config(page_title="Music Key Finder", page_icon=":musical_score:", layout="wide")

    st.title("Music Key Finder")
    st.caption("Explore scales, diatonic chords, progressions, and color chords by key.")

    input_col_1, input_col_2 = st.columns([1, 1])
    with input_col_1:
        root = st.selectbox("Root note", ROOT_OPTIONS, index=ROOT_OPTIONS.index("C"))
    with input_col_2:
        mode = st.selectbox("Mode", ["major", "minor"])

    pattern, chord_pattern, romans, progressions = get_mode_data(mode)
    scale = build_scale(root, pattern)
    chords = build_chords(scale, chord_pattern)
    relative_key = get_relative_key(scale, mode)

    show_key_summary(root, mode, scale, chords, relative_key)

    chords_tab, chord_finder_tab, progressions_tab, extended_tab, tonicization_tab, modal_tab, borrowed_tab = st.tabs(
        [
            "Scale & Chords",
            "Chord Finder",
            "Progressions",
            "Extended / Altered Chords",
            "Tonicization",
            "Modal Interchange",
            "Borrowed Chords",
        ]
    )

    with chords_tab:
        st.subheader("Scale & Chords")
        chord_rows = build_diatonic_chord_rows(romans, scale, chords)
        st.dataframe(
            chord_rows,
            width="stretch",
            hide_index=True,
        )

    with chord_finder_tab:
        st.subheader("Chord Finder")

        finder_col_1, finder_col_2, finder_col_3 = st.columns(3)
        with finder_col_1:
            chord_root = st.selectbox("Root", ROOT_OPTIONS, index=ROOT_OPTIONS.index(root))
        with finder_col_2:
            chord_quality = st.selectbox("Mode", get_chord_quality_names())
        with finder_col_3:
            chord_extension = st.selectbox("Extended / Altered", get_chord_extension_names())

        chord_result = build_chord_finder_result(chord_root, chord_quality, chord_extension)
        st.subheader(chord_result["symbol"])
        st.dataframe(
            chord_result["rows"],
            width="stretch",
            hide_index=True,
        )
        st.markdown(
            render_keyboard_html(chord_result["tones"], title=f"Keyboard: {chord_result['symbol']}"),
            unsafe_allow_html=True,
        )
        components.html(
            render_fretboard_html(
                chord_result["tones"],
                root_note=chord_root,
                title=f"Guitar Fretboard: {chord_result['symbol']}",
            ),
            height=430,
            scrolling=True,
        )

    with progressions_tab:
        st.subheader("Common Progressions")
        st.dataframe(
            build_progression_rows(progressions, chords, root),
            width="stretch",
            hide_index=True,
        )

    with extended_tab:
        st.subheader("Extended Chords")
        st.dataframe(
            build_extended_chord_rows(romans, scale, chord_pattern),
            width="stretch",
            hide_index=True,
        )

        with st.expander("Altered dominant colors"):
            st.dataframe(
                build_altered_dominant_rows(root),
                width="stretch",
                hide_index=True,
            )

    with tonicization_tab:
        st.subheader("Tonicization")

        tonicization_options = ["None"] + chords[1:]
        selected_chord = st.selectbox("Tonicize a chord", tonicization_options)

        if selected_chord != "None":
            notes_system = choose_note_system(root)
            target_root = get_chord_root(selected_chord)
            secondary_dominant = get_dominant_for_target(target_root, notes_system)
            tritone_sub = get_tritone_substitution_for_target(target_root, notes_system)

            dominant_col, tritone_col = st.columns(2)
            with dominant_col:
                st.success(f"{secondary_dominant} -> {selected_chord}")
            with tritone_col:
                st.info(f"{tritone_sub} -> {selected_chord}")
        else:
            st.write("Choose a non-tonic chord to see its secondary dominant and tritone substitute.")

        with st.expander("All secondary dominants"):
            st.dataframe(
                build_secondary_dominant_rows(scale, root),
                width="stretch",
                hide_index=True,
            )

    with modal_tab:
        st.subheader("Modal Interchange")
        st.dataframe(
            build_modal_interchange_rows(root),
            width="stretch",
            hide_index=True,
        )

    with borrowed_tab:
        st.subheader("Borrowed Chords")
        st.dataframe(
            build_borrowed_chord_rows(root, chords),
            width="stretch",
            hide_index=True,
        )


if __name__ == "__main__":
    main()
