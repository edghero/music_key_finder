from html import escape

from theory.scales import get_note_index

WHITE_KEYS = [
    ("C", 0),
    ("D", 2),
    ("E", 4),
    ("F", 5),
    ("G", 7),
    ("A", 9),
    ("B", 11),
]

BLACK_KEYS = [
    ("C#/Db", 1, 9),
    ("D#/Eb", 3, 23),
    ("F#/Gb", 6, 51),
    ("G#/Ab", 8, 65),
    ("A#/Bb", 10, 79),
]


def render_keyboard_html(highlight_notes):
    highlighted_indexes = {get_note_index(note) for note in highlight_notes}

    white_keys_html = []
    for note_name, note_index in WHITE_KEYS:
        is_highlighted = note_index in highlighted_indexes
        classes = "piano-key white-key highlighted" if is_highlighted else "piano-key white-key"
        label = note_name if is_highlighted else ""
        white_keys_html.append(
            f'<div class="{classes}"><span>{escape(label)}</span></div>'
        )

    black_keys_html = []
    for note_name, note_index, left_percent in BLACK_KEYS:
        is_highlighted = note_index in highlighted_indexes
        classes = "piano-key black-key highlighted" if is_highlighted else "piano-key black-key"
        label = note_name if is_highlighted else ""
        black_keys_html.append(
            f'<div class="{classes}" style="left: {left_percent}%"><span>{escape(label)}</span></div>'
        )

    return f"""
    <style>
        .piano-wrapper {{
            margin-top: 1rem;
            width: 100%;
            max-width: 760px;
        }}

        .piano-title {{
            margin: 0 0 0.45rem 0;
            font-size: 1rem;
            font-weight: 600;
        }}

        .piano {{
            position: relative;
            display: flex;
            height: 180px;
            width: 100%;
            border: 1px solid #c7cbd1;
            border-radius: 8px;
            overflow: hidden;
            background: #f8fafc;
        }}

        .piano-key {{
            box-sizing: border-box;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            font-size: 0.82rem;
            font-weight: 700;
        }}

        .white-key {{
            flex: 1;
            height: 100%;
            padding-bottom: 0.85rem;
            color: #1f2937;
            background: #ffffff;
            border-right: 1px solid #d7dce2;
        }}

        .white-key:last-child {{
            border-right: 0;
        }}

        .black-key {{
            position: absolute;
            top: 0;
            z-index: 2;
            width: 9%;
            height: 62%;
            transform: translateX(-50%);
            padding-bottom: 0.55rem;
            color: #f8fafc;
            background: #111827;
            border-radius: 0 0 6px 6px;
            box-shadow: 0 3px 8px rgba(15, 23, 42, 0.35);
        }}

        .white-key.highlighted {{
            background: #d9f99d;
            color: #365314;
        }}

        .black-key.highlighted {{
            background: #2563eb;
            color: #eff6ff;
        }}

        .piano-key span {{
            line-height: 1;
            text-align: center;
        }}
    </style>
    <div class="piano-wrapper">
        <p class="piano-title">Keyboard</p>
        <div class="piano">
            {''.join(white_keys_html)}
            {''.join(black_keys_html)}
        </div>
    </div>
    """
