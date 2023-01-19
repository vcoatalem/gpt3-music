import gpt
import midi
import music


# 1. Ask gpt to create a chord progression and parse the result
openai_chords = gpt.get_chord_progression(nb_chords=4, track_description="melancholic song")

print("notes parsed from gpt:", openai_chords)

# 2. Generate chords components using pychord
chords = list(map(lambda note: music.create_chord(note), openai_chords))
chords_components = list(map(lambda chord: chord.components_with_pitch(3), chords))

print("chord components:", chords_components)

# 3. Output to a midi file using MIDIUtils
midi.create_midi_file(chords_components, midi.create_output_filename(chords))

#midi.play_midi_file("out.mid")
#play_midi_file("Z:\Code\gpt-experiments\out.mid")