import pychord

def create_chord(root_note="C", base_scale="Cmaj", root_pitch=3):
    print(f"create chord for root note: {root_note}")
    chord = pychord.Chord(root_note)
    print(chord.quality)

    # add 7th note to chord if on the degree V
    if (chord == pychord.Chord.from_note_index(5, chord.quality, base_scale) and "7" not in root_note):
        chord = pychord.Chord(root_note + "7")
    return chord.components_with_pitch(root_pitch)
