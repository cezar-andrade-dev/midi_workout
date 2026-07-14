from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

# ==========================================================
# PROJECT SETTINGS
# ==========================================================

OUTPUT_FILE = "circle_of_fourths_workout.mid"

BPM = 60
TICKS_PER_BEAT = 480

NUM_REPETITIONS = 3

CHORD_DURATION = 1.0      # seconds
ARPEGGIO_NOTE_DURATION = 0.5  # seconds

# ==========================================================
# HARMONIC SEQUENCES
# ==========================================================

# Major chords used during exercise periods
EXERCISE_ROOTS = [
    "C", "F", "Bb", "Eb", "Ab", "Db"
]

# Minor chords used during rest periods
REST_ROOTS = [
    "Gb", "B", "E", "A", "D", "G"
]

# ==========================================================
# CHORD INTERVALS (in semitones from the root)
# ==========================================================


MAJOR_INTERVALS = {"third": 4, "fifth": 7}
MINOR_INTERVALS = {"third": 3, "fifth": 7}
AUGMENTED_INTERVALS = {"third": 4, "fifth": 8}
DIMINISHED_INTERVALS = {"third": 3, "fifth": 6}
MAJOR_SEVEN = {"third": 4, "fifth": 7, "seventh": 11}
MINOR_SEVEN = {"third": 4, "fifth": 7, "seventh": 10}

# ==========================================================
# MIDI NOTE MAPPING
# ==========================================================

NOTE_TO_MIDI = {
    "C": 60,
    "Db": 61,
    "D": 62,
    "Eb": 63,
    "E": 64,
    "F": 65,
    "Gb": 66,
    "G": 67,
    "Ab": 68,
    "A": 69,
    "Bb": 70,
    "B": 71
}

# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def seconds_to_ticks(seconds: float) -> int:
    """
    Converts seconds to MIDI ticks, based on the current BPM.

    ticks = seconds * (ticks_per_beat * beats_per_second)
          = seconds * (TICKS_PER_BEAT * BPM / 60)

    This works for any BPM value, not just BPM = 60.
    """
    ticks_per_second = TICKS_PER_BEAT * BPM / 60
    return int(seconds * ticks_per_second)


def add_single_note(
    track: MidiTrack,
    note: int,
    duration_seconds: float,
    velocity: int = 70
) -> None:
    """
    Adds a single MIDI note to the track.
    """

    duration_ticks = seconds_to_ticks(duration_seconds)

    track.append(
        Message(
            "note_on",
            note=note,
            velocity=velocity,
            time=0
        )
    )

    track.append(
        Message(
            "note_off",
            note=note,
            velocity=0,
            time=duration_ticks
        )
    )


def add_chord(
    track: MidiTrack,
    notes: list[int],
    duration_seconds: float,
    velocity: int = 90
) -> None:
    """
    Adds a chord where all notes start simultaneously.
    """

    duration_ticks = seconds_to_ticks(duration_seconds)

    # Turn notes on
    for note in notes:
        track.append(
            Message(
                "note_on",
                note=note,
                velocity=velocity,
                time=0
            )
        )

    # Turn notes off
    first_note = True

    for note in notes:
        track.append(
            Message(
                "note_off",
                note=note,
                velocity=0,
                time=duration_ticks if first_note else 0
            )
        )

        first_note = False


# ==========================================================
# MUSICAL BUILDING BLOCKS
# ==========================================================

def add_triad_section(
    track: MidiTrack,
    root_name: str,
    third_interval: int,
    fifth_interval: int,
    seventh_interval: int
) -> None:
    """
    Creates a 5-second block built from a triad (root, third, fifth):

        1 second  -> chord
        4 seconds -> arpeggio (root, third, fifth, third) x2

    Used for both major (exercise) and minor (rest) sections,
    the only difference being the third/fifth intervals passed in.
    """

    root = NOTE_TO_MIDI[root_name]
    third = root + third_interval
    fifth = root + fifth_interval
    seventh = root + seventh_interval

    add_chord(
        track,
        [root, third, fifth, seventh],
        CHORD_DURATION
    )

    arpeggio_pattern = [root, third, fifth, seventh] * 2

    for note in arpeggio_pattern:
        add_single_note(
            track,
            note,
            ARPEGGIO_NOTE_DURATION
        )


def add_major_section(track: MidiTrack, root_name: str) -> None:
    """
    5-second exercise block using an augmented triad.

    Example (C Major):
        Chord: C E G
        Arpeggio: C E G E | C E G E
    """
    add_triad_section(
        track,
        root_name,
        third_interval=MAJOR_INTERVALS["third"],
        fifth_interval=MAJOR_INTERVALS["fifth"],
       
    )


def add_minor_section(track: MidiTrack, root_name: str) -> None:
    
    add_triad_section(
        track,
        root_name,
        third_interval=MINOR_INTERVALS["third"],
        fifth_interval=MINOR_INTERVALS["fifth"]
    )


# ==========================================================
# MIDI FILE CREATION
# ==========================================================

def create_workout_midi() -> None:
    """
    Generates the complete workout MIDI file.

    Workout structure:

    Exercise Phase (30 seconds)
        C  -> 5 sec
        F  -> 5 sec
        Bb -> 5 sec
        Eb -> 5 sec
        Ab -> 5 sec
        Db -> 5 sec

    Rest Phase (30 seconds)
        Gbm -> 5 sec
        Bm  -> 5 sec
        Em  -> 5 sec
        Am  -> 5 sec
        Dm  -> 5 sec
        Gm  -> 5 sec

    Repeated NUM_REPETITIONS times.
    """

    midi = MidiFile()
    track = MidiTrack()

    midi.tracks.append(track)

    # Tempo configuration
    track.append(
        MetaMessage(
            "set_tempo",
            tempo=bpm2tempo(BPM),
            time=0
        )
    )

    # Acoustic Grand Piano
    track.append(
        Message(
            "program_change",
            program=0,
            time=0
        )
    )

    for _ in range(NUM_REPETITIONS):

        # Exercise phase
        for root in EXERCISE_ROOTS:
            add_major_section(track, root)

        # Rest phase
        for root in REST_ROOTS:
            add_minor_section(track, root)

    try:
        midi.save(OUTPUT_FILE)
    except OSError as error:
        print(f"Failed to save MIDI file '{OUTPUT_FILE}': {error}")
        return

    print(f"Workout MIDI successfully created: {OUTPUT_FILE}")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    create_workout_midi()
