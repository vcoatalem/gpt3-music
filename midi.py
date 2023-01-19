import pygame.mixer
import pygame.midi

import time

from midiutil import MIDIFile

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


def play_midi_file(midi_filename):
    pygame.midi.init()
    pygame.mixer.init()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.set_volume(60)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        time.sleep(1)
