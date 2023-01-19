import gpt
import midi
import music


# 1. Ask gpt to create a chord progression and parse the result
openai_chord = gpt.get_chord_progression(nb_chords=4, track_description="melancholic song")

#print(response.choices[0].text)

print("notes parsed from gpt:", openai_chord)

# 2. Generate chords components using pychord
chords_components = list(map(lambda note: music.create_chord(note), openai_chord))

print("chord components:", chords_components)

# 3. Output to a midi file using MIDIUtils
midi.create_midi_file(chords_components)

midi.play_midi_file("out.mid")
#play_midi_file("Z:\Code\gpt-experiments\out.mid")