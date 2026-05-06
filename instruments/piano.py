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
    ("C#/Db", 1, 0),
    ("D#/Eb", 3, 1),
    ("F#/Gb", 6, 3),
    ("G#/Ab", 8, 4),
    ("A#/Bb", 10, 5),
]


def render_keyboard_html(highlight_notes, title="Keyboard", octaves=2):
    highlighted_indexes = {get_note_index(note) for note in highlight_notes}
    total_white_keys = len(WHITE_KEYS) * octaves
    white_key_width = 100 / total_white_keys
    black_key_width = white_key_width * 0.62

    white_keys_html = []
    for octave in range(octaves):
        for note_name, note_index in WHITE_KEYS:
            is_highlighted = note_index in highlighted_indexes
            classes = "piano-key white-key highlighted" if is_highlighted else "piano-key white-key"
            label = note_name if is_highlighted else ""
            white_keys_html.append(
                f'<div class="{classes}"><span>{escape(label)}</span></div>'
            )

    black_keys_html = []
    for octave in range(octaves):
        octave_offset = octave * len(WHITE_KEYS)

        for note_name, note_index, white_key_position in BLACK_KEYS:
            is_highlighted = note_index in highlighted_indexes
            classes = "piano-key black-key highlighted" if is_highlighted else "piano-key black-key"
            label = note_name if is_highlighted else ""
            left_percent = (octave_offset + white_key_position + 1) * white_key_width
            black_keys_html.append(
                f'<div class="{classes}" style="left: {left_percent}%; width: {black_key_width}%">'
                f"<span>{escape(label)}</span></div>"
            )

    return f"""
    <style>
        .piano-wrapper {{
            margin-top: 1rem;
            width: 100%;
            max-width: 980px;
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
            position: relative;
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
            height: 62%;
            transform: translateX(-50%);
            padding-bottom: 0.55rem;
            color: #f8fafc;
            background: #111827;
            border-radius: 0 0 6px 6px;
            box-shadow: 0 3px 8px rgba(15, 23, 42, 0.35);
        }}

        .white-key.highlighted {{
            background: #ffffff;
            color: #92400e;
            box-shadow: inset 0 -5px 0 #f59e0b;
        }}

        .black-key.highlighted {{
            background: #111827;
            color: #fde68a;
            outline: 3px solid #f59e0b;
            outline-offset: -3px;
        }}

        .piano-key span {{
            line-height: 1;
            text-align: center;
        }}
    </style>
    <div class="piano-wrapper">
        <p class="piano-title">{escape(title)}</p>
        <div class="piano">
            {''.join(white_keys_html)}
            {''.join(black_keys_html)}
        </div>
    </div>
    """
