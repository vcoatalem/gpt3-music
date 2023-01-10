import openai
import re
import pychord

from midiutil import MIDIFile

# process is as follow:

# 1. Generate chord progression through OpenAI API and parse it
# 2. Create chords using pychord
# 3. Create midi track from chord components


def get_chord_progression(prompt):
    
    open_ai_api_key = "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"
    # Initialize the OpenAI API
    openai.api_key = open_ai_api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0
    )
    print(response.choices[0])
    note_parsed = parse_notes(response.choices[0].text)
    return note_parsed

def parse_notes(string):
    notes = re.findall(r'[A-G](?:#|b)?[ ]*(?:min|maj|minor|major|m|M)?[0-9]?', string)
    return notes

def create_chord(root_note, root_pitch=3):
    chord = pychord.Chord(root_note)
    return chord.components_with_pitch(root_pitch)

# https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
def NoteToMidi(KeyOctave):

    NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # KeyOctave is formatted like 'C#3'
    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]   # eg 3, 4
    answer = -1

    try:
        if 'b' in key:
            pos = NOTES_FLAT.index(key)
        else:
            pos = NOTES_SHARP.index(key)
    except:
        print('The key is not valid', key)
        return answer

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer

def create_midi_file(chords_components, filename_output="out.mid"):

    track    = 0
    channel  = 0
    time     = 0    # In beats
    time_unit = 4   # 1 grid
    duration = 4    # In beats
    tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, chord in enumerate(chords_components):
        degrees = list(map(lambda note: NoteToMidi(note), chord))
        print(degrees)
        for degree in degrees:
            MyMIDI.addNote(track, channel, degree, time + i * time_unit, duration, volume)

    with open(filename_output, "wb") as output_file:
        MyMIDI.writeFile(output_file)
  




# 1. Ask gpt to create a chord progression and parse the result
openai_chord = get_chord_progression('Write me a melancholic chord progression using letters')

#print(response.choices[0].text)

print("notes parsed from gpt:", openai_chord)

# 2. Generate chords components using pychord
chords_components = list(map(lambda note: create_chord(note), openai_chord))

print("chord components:", chords_components)

# 3. Output to a midi file using MIDIUtils
create_midi_file(chords_components)
