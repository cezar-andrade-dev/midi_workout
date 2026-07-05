# MIDI Workout Generator

Generate MIDI ear-training exercises based on the circle of fourths, alternating augmented chords (exercise) and diminished chords (rest).

## Overview

This script produces a MIDI file structured as a workout routine:

- **Exercise phase (30s):** augmented chords built on the roots C, F, Bb, Eb, Ab, Db, each held for 1 second, followed by a 4-second arpeggio.
- **Rest phase (30s):** diminished chords built on the roots Gb, B, E, A, D, G, following the same 1s chord + 4s arpeggio structure.

The full exercise/rest cycle is repeated `NUM_REPETITIONS` times (3 by default), producing a 3-minute workout file.

## Requirements

- Python >= 3.13, < 4.0
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

```bash
git clone https://github.com/cezar-andrade-dev/midi-workout.git
cd midi-workout
poetry install
```

## Usage

Run the generator with:

```bash
poetry run python main.py
```

This will create a `circle_of_fourths_workout.mid` file in the project root, which you can open in any DAW (Ableton, Logic, GarageBand, etc.) or MIDI player.

## Configuration

The main parameters can be adjusted at the top of the script:

| Parameter                | Description                                  | Default |
|---------------------------|-----------------------------------------------|---------|
| `BPM`                     | Tempo in beats per minute                    | `60`    |
| `TICKS_PER_BEAT`          | MIDI resolution                              | `480`   |
| `NUM_REPETITIONS`         | Number of exercise/rest cycles               | `3`     |
| `CHORD_DURATION`          | Duration of each chord, in seconds           | `1.0`   |
| `ARPEGGIO_NOTE_DURATION`  | Duration of each arpeggio note, in seconds   | `0.5`   |

## Project Structure

```
midi-workout/
├── main.py             # Script entry point and MIDI generation logic
├── pyproject.toml       # Project metadata and dependencies (Poetry)
├── poetry.lock
├── README.md
├── LICENSE
└── .gitignore
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
