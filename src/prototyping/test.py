import numpy as np
interval = [1, 5, 8]

def midi_to_note_name(midi):
    """Convert midi note to note name."""
    note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    # octave = (midi-21)//12
    note = (midi-21)%12
    return note#note_names[note]

current_chord = [22,26,29]

current_chord=[midi_to_note_name(note) for note in current_chord]
out=[]
l=[]
cols=[]
note_rep=[]
for root in range(21,108+1):
    cols.append([root+i for i in interval]) # actual midi notes
    note_rep.append(sorted([midi_to_note_name(root+i) for i in interval])) # sort the notes in a chord

for i in range(len(current_chord)):
    chord_cmp = np.roll(np.array(note_rep),i,axis=1) - sorted(current_chord) # circular shift the note representation of the chords
    idx = np.count_nonzero(chord_cmp,axis=1) == len(current_chord)-1 # find the index of the chord that has the same notes as the current chord, except for one
    out.append(np.array(cols)[idx])
    l.append(np.array(note_rep)[idx])

