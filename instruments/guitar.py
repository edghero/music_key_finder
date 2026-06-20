from html import escape

from theory.scales import NOTES_SHARP, get_note_index

STANDARD_TUNING = [
    ("e", "E"),
    ("B", "B"),
    ("G", "G"),
    ("D", "D"),
    ("A", "A"),
    ("E", "E"),
]


def get_fret_note(open_note, fret):
    note_index = (get_note_index(open_note) + fret) % len(NOTES_SHARP)
    return NOTES_SHARP[note_index]


def render_fretboard_html(highlight_notes, root_note=None, title="Guitar Fretboard", frets=12):
    highlighted_notes = {get_note_index(note): note for note in highlight_notes}
    root_index = get_note_index(root_note) if root_note else None
    fret_numbers = "".join(
        f'<div class="fret-number">{fret}</div>'
        for fret in range(frets + 1)
    )

    string_rows = []
    for string_label, open_note in STANDARD_TUNING:
        fret_cells = []

        for fret in range(frets + 1):
            note = get_fret_note(open_note, fret)
            note_index = get_note_index(note)
            is_highlighted = note_index in highlighted_notes
            is_root = root_index == note_index
            classes = ["fret-cell"]

            if fret == 0:
                classes.append("open-fret")
            if is_highlighted:
                classes.append("highlighted")
            if is_root:
                classes.append("root-note")

            label = highlighted_notes.get(note_index, "")
            fret_cells.append(
                f'<div class="{" ".join(classes)}">'
                f'<span class="string-line"></span>'
                f'<span class="note-dot">{escape(label)}</span>'
                f"</div>"
            )

        string_rows.append(
            f"""
            <div class="fretboard-row">
                <div class="string-label">{escape(string_label)}</div>
                <div class="frets">{''.join(fret_cells)}</div>
            </div>
            """
        )

    marker_cells = []
    for fret in range(frets + 1):
        marker = "dot" if fret in [3, 5, 7, 9] else ""
        marker = "double-dot" if fret == 12 else marker
        marker_cells.append(f'<div class="fret-marker {marker}"></div>')

    return f"""
    <style>
        .guitar-wrapper {{
            margin-top: 1.25rem;
            width: 100%;
            max-width: 980px;
        }}

        .guitar-title {{
            margin: 0 0 0.45rem 0;
            font-size: 1rem;
            font-weight: 600;
        }}

        .fretboard {{
            width: 100%;
            overflow-x: auto;
            padding: 0.75rem 0.75rem 0.6rem;
            border: 1px solid #c7cbd1;
            border-radius: 8px;
            background: #f9fafb;
        }}

        .fret-numbers,
        .marker-row,
        .frets {{
            display: grid;
            grid-template-columns: 0.8fr repeat({frets}, minmax(44px, 1fr));
            min-width: 720px;
        }}

        .fret-numbers,
        .marker-row {{
            margin-left: 2rem;
        }}

        .fret-number {{
            min-height: 1.15rem;
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 700;
            text-align: center;
        }}

        .fretboard-row {{
            display: grid;
            grid-template-columns: 2rem 1fr;
            align-items: center;
        }}

        .string-label {{
            color: #475569;
            font-size: 0.78rem;
            font-weight: 700;
            text-align: center;
        }}

        .fret-cell {{
            position: relative;
            box-sizing: border-box;
            min-height: 42px;
            border-left: 2px solid #c9a227;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .fret-cell:last-child {{
            border-right: 2px solid #c9a227;
        }}

        .open-fret {{
            border-left: 5px solid #475569;
            background: rgba(226, 232, 240, 0.45);
        }}

        .string-line {{
            position: absolute;
            left: 0;
            right: 0;
            top: 50%;
            height: 2px;
            transform: translateY(-50%);
            background: #94a3b8;
        }}

        .note-dot {{
            position: relative;
            z-index: 1;
            display: none;
            min-width: 30px;
            height: 30px;
            padding: 0 0.35rem;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            background: #0f172a;
            color: #f8fafc;
            font-size: 0.72rem;
            font-weight: 800;
            line-height: 30px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.24);
        }}

        .highlighted .note-dot {{
            display: inline-flex;
        }}

        .root-note .note-dot {{
            background: #f59e0b;
            color: #111827;
            outline: 2px solid #92400e;
            outline-offset: 1px;
        }}

        .fret-marker {{
            min-height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .fret-marker.dot::after {{
            content: "";
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #cbd5e1;
        }}

        .fret-marker.double-dot::after {{
            content: "";
            width: 18px;
            height: 7px;
            border-radius: 999px;
            background: linear-gradient(90deg, #cbd5e1 0 7px, transparent 7px 11px, #cbd5e1 11px 18px);
        }}
    </style>
    <div class="guitar-wrapper">
        <p class="guitar-title">{escape(title)}</p>
        <div class="fretboard">
            <div class="fret-numbers">{fret_numbers}</div>
            {''.join(string_rows)}
            <div class="marker-row">{''.join(marker_cells)}</div>
        </div>
    </div>
    """
