# Music Key Finder

A Streamlit music theory helper for exploring keys, scales, diatonic chords, progressions, tonicization, tritone substitutions, modal interchange, borrowed chords, and extended or altered chord colors.

## Run The Streamlit App

```zsh
source venv/bin/activate
streamlit run app.py
```

## Project Structure

```text
music_key_finder/
├── app.py
├── main.py
├── theory/
├── instruments/
├── data/
└── README.md
```

- `app.py`: Streamlit UI layer.
- `main.py`: Optional terminal interface.
- `theory/`: Core music logic.
- `instruments/`: Future piano and guitar visualizations.
- `data/`: Future saved scales, progressions, or exports.
