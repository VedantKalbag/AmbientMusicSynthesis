import numpy as np
import pandas as pd
import random as rm
from collections import OrderedDict

from collections import Counter
# np.random.seed(42)

import os
# print(os.getcwd())

major_keys = OrderedDict({
                'F':['Bb','F','C',"Dm"], # Each list contains keys that it can transition to (the first 3 are major and the last is minor)
                'C':['F','C','G',"Am"],
                'G':['C','G','D',"Em"],
                'D':['G','D','A',"Bm"],
                'A':['D','A','E',"F#m"],
                'E':['A','E','B',"C#m"],
                'B':['E','B','Gb',"G#m"],
                'Gb':['B','Gb','Db',"Ebm"],
                'Db':['Gb','Db','Ab',"Bbm"], 
                'Ab':['Db','Ab','Eb',"Fm"], 
                'Eb':['Ab','Eb','Bb',"Cm"], 
                'Bb':['Eb','Bb','F',"Gm"],
                'Am':["C","C","C","C"], # TODO: Consider adding another minor key as the last element of this list
                'Em':["G","G","G","G"],
                'Bm':["D","D","D","D"],
                'F#m':["A","A","A","A"],
                'C#m':["Eb","Eb","Eb","Eb"],
                'G#m':["B","B","B","B"],
                'Ebm':["Gb","Gb","Gb","Gb"], 
                'Bbm':["Db","Db","Db","Db"], 
                'Fm':["Ab","Ab","Ab","Ab"], 
                'Cm':["Eb","Eb","Eb","Eb"],
                'Gm':["Bb","Bb","Bb","Bb"],
                'Dm':["F","F","F","F"]
            })
minor_keys = OrderedDict({
                'Am':['Dm','Am','Em',"C"],
                'Em':['Am','Em','Bm',"G"],
                'Bm':['Em','Bm','F#m',"D"],
                'F#m':['Bm','F#m','C#m',"A"],
                'C#m':['F#m','C#m','G#m',"Eb"],
                'G#m':['C#m','G#m','Ebm',"B"],
                'Ebm':['G#m','Ebm','Bbm',"Gb"], 
                'Bbm':['Ebm','Bbm','Fm',"Db"], 
                'Fm':['Bbm','Fm','Cm',"Ab"], 
                'Cm':['Fm','Cm','Gm',"Eb"],
                'Gm':['Cm','Gm','Dm',"Bb"],
                'Dm':['Gm','Dm','Am',"F"],
                'F':["Dm","Dm","Dm","Dm"], 
                'C':["Am","Am","Am","Am"],
                'G':["Em","Em","Em","Em"],
                'D':["Bm","Bm","Bm","Bm"],
                'A':["F#m","F#m","F#m","F#m"],
                'E':["C#m","C#m","C#m","C#m"],
                'B':["G#m","G#m","G#m","G#m"],
                'Gb':["Ebm","Ebm","Ebm","Ebm"],
                'Db':["Bbm","Bbm","Bbm","Bbm"], 
                'Ab':["Fm","Fm","Fm","Fm"], 
                'Eb':["Cm","Cm","Cm","Cm"], 
                'Bb':["Gm","Gm","Gm","Gm"]
                })
transition_probabilities=[0.3,0.3,0.3,0.1]



# # MARKOV CHAIN FOR CHORDS
# # ----------------------------------------------------------------------
# def predict_next_state(chord:str, segment:int=1):
#     """Predict next chord based on current state."""
#         # read file
#     data = pd.read_csv('resources/Liverpool_band_chord_sequence.csv')
#     # ----------------------------------------------------------------------
#     n = 3
#     chords = data['chords'].values
#     ngrams = zip(*[chords[i:] for i in range(n)])
#     bigrams = [" ".join(ngram) for ngram in ngrams]
#     # create list of bigrams which stats with current chord
#     bigrams_with_current_chord = [bigram for bigram in bigrams if bigram.split(' ')[0]==chord]
#     # count appearance of each bigram
#     count_appearance = dict(Counter(bigrams_with_current_chord))
#     # convert apperance into probabilities
#     for ngram in count_appearance.keys():
#         count_appearance[ngram] = count_appearance[ngram]/len(bigrams_with_current_chord)
    
#     # create list of possible options for the next chord
#     options = [key.split(' ')[1] for key in count_appearance.keys()]
#     # print(options)
#     # create  list of probability distribution
#     probabilities = list(count_appearance.values())
#     # return random prediction
#     return np.random.choice(options, p=probabilities)

# # ----------------------------------------------------------------------
# def generate_sequence(chord:str=None, length:int=30):
#     """Generate sequence of defined length."""
#     # create list to store future chords
#     chords = []
#     chords.append(chord)
#     for n in range(length-1):
#         # append next chord for the list
#         chords.append(predict_next_state(chord))
#         # use last chord in sequence to predict next chord
#         chord = chords[-1]
#     return chords
def get_note_density(sequence, initial_state=3, seed="NA", transition_probs=[0.2,0.3,0.3,0.1,0.1]):
    assert sum(transition_probs) == 1
    states = [1,2,3,4,5]
    densities=[initial_state]
    for i in range(len(sequence)-1):
        densities.append(np.random.choice(states, p=transition_probs))
    return densities

midi_notes = list(range(21,108+1))

def get_major_scale(midi_note):
    return [midi_note, midi_note + 2, midi_note + 4, midi_note + 5, midi_note + 7, midi_note + 9, midi_note + 11, midi_note + 12]

def get_minor_scale(midi_note):
    return [midi_note, midi_note + 2, midi_note + 3, midi_note + 5, midi_note + 7, midi_note + 8, midi_note + 10, midi_note + 12]

def get_roots_search_space(midi_note):
    major_scale = get_major_scale(midi_note)
    # print (major_scale)
    minor_scale = get_minor_scale(midi_note)
    # print(minor_scale)
    major_roots = np.array([major_scale[3-1], major_scale[-3]-12])
    # print (major_roots)
    minor_roots = np.array([minor_scale[3-1], minor_scale[-3]-12])
    # print(minor_roots)
    return np.append(major_roots, minor_roots)

def get_major_intervals(num_notes):
    match num_notes:
        case 1:
            return np.array(rm.choice([[1],[5]])) # root or fifth
        case 2:
            return np.array([1,8]) # root,fifth
        case 3:
            return np.array([1,5,8]) # root, third, fifth
        case 4:
            return np.array([1,5,8,13]) # root, third, fifth, octave
        case 5:
            return np.array([1,5,8,13,rm.choice([20,-4])]) # root, third, fifth, octave, fifth of higher/lower octave

def get_minor_intervals(num_notes):
    match num_notes:
        case 1:
            return np.array(rm.choice([[1],[4]])) # root or fifth
        case 2:
            return np.array([1,8]) # root,fifth
        case 3:
            return np.array([1,4,8]) # root, third, fifth
        case 4:
            return np.array([1,4,8,13]) # root, third, fifth, octave
        case 5:
            return np.array([1,4,8,13,rm.choice([20,-4])]) # root, third, fifth, octave, fifth of higher/lower octave

def get_chord_search_space(midi_note, num_notes=3):
    roots = get_roots_search_space(midi_note)
    major_interval = get_major_intervals(num_notes)
    minor_interval = get_minor_intervals(num_notes)
    major_chords = []
    minor_chords = []
    for root in roots:
        major_chords.append(root + major_interval)
        minor_chords.append(root + minor_interval)
    # print(major_chords)
    # print(minor_chords)
    # print([number_to_note(num)[0] for num in major_chords])
    # print([number_to_note(num)[0] for num in minor_chords])
    return np.append(major_chords, minor_chords, axis=0)

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

def number_to_note(number: int) -> tuple:
    octave = number // NOTES_IN_OCTAVE
    # assert octave in OCTAVES
    # assert 0 <= number <= 127
    note = NOTES[number % NOTES_IN_OCTAVE]

    return number % NOTES_IN_OCTAVE, note, octave # Note number (0-11), note name, octave

def note_to_number(note: str, octave: int) -> int:
    assert note in NOTES
    # assert octave in OCTAVES

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    # assert 0 <= note <= 127

    return note

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_next_chord(current_chord):
    sorted_current_chord=sorted([number_to_note(note)[0] for note in current_chord])
    possible_chords=[]
    nearest_chords=[]
    chords_midi=get_chord_search_space(current_chord[0])
    for chord in get_chord_search_space(current_chord[0]):
        possible_chords.append([number_to_note(note)[0] for note in chord])
        for i in range(len(current_chord)):
            mask = np.count_nonzero(np.roll(np.array([number_to_note(note)[0] for note in chord]),i) - sorted_current_chord) == 1
            if np.all(mask) != False:
                # print(chord)
                nearest_chords.append(chord)
    return rm.choice(nearest_chords), np.array(nearest_chords)
    
# Random choice using circle of fifths only, using only the root of every key
def generate_sequence_v1(starting_key, length): 
    """Generate sequence of defined length."""
    # create list to store future chords
    chords = []
    current_key = starting_key
    # n_chords = rm.randint(2,10)
    # generate chords progressions for current_key

    chords.append(current_key)
    if current_key in list(major_keys.keys())[:12]:
        for n in range(length):
            # append next chord for the list
            choice = np.random.choice(major_keys[current_key], p=transition_probabilities)
            while (choice == current_key):
                choice = np.random.choice(major_keys[current_key], p=transition_probabilities)
            chords.append(choice)
            # use last chord in sequence to predict next chord
            current_key = chords[-1]
    elif current_key in list(minor_keys.keys())[:12]:
        for n in range(length):
            # append next chord for the list
            choice = np.random.choice(minor_keys[current_key], p=transition_probabilities)
            while (choice == current_key):
                choice = np.random.choice(minor_keys[current_key], p=transition_probabilities)
            chords.append(choice)
            # use last chord in sequence to predict next chord
            current_key = chords[-1]
        
    return chords

# Function to generate sequence of chords using circle of fifths and nearest chords (single note change) randomly
def generate_sequence_v2(starting_key, length):
    """Generate sequence of defined length."""
    # create list to store future chords
    chords = []
    current_key = starting_key
    # n_chords = rm.randint(2,10)
    # generate chords progressions for current_key

    chords.append(current_key)
    if current_key in list(major_keys.keys())[:12]:
        for n in range(length):
            # append next chord for the list
            choice = np.random.choice(major_keys[current_key], p=transition_probabilities)
            while (choice == current_key):
                choice = np.random.choice(major_keys[current_key], p=transition_probabilities)
            chords.append(choice)
            # use last chord in sequence to predict next chord
            current_key = chords[-1]
    elif current_key in list(minor_keys.keys())[:12]:
        for n in range(length):
            # append next chord for the list
            choice = np.random.choice(minor_keys[current_key], p=transition_probabilities)
            while (choice == current_key):
                choice = np.random.choice(minor_keys[current_key], p=transition_probabilities)
            chords.append(choice)
            # use last chord in sequence to predict next chord
            current_key = chords[-1]
        
    return chords

# MARKOV CHAIN FOR CHORD LENGTHS
def get_length_sequence(initial_state, n_steps,transitionMatrix, seed="NA"):
    """Return sequence of chord lengths based on initial state and transition matrix."""
    # The statespace
    states = ["VS","S","M","L","VL"]
    # Possible sequences of events
    # transitionName = [["VSVS","VSS","VSM","VSL","VSVL"],["SVS","SS","SM","SL","SVL"],["MVS","MS","MM","ML","MVL"],["LVS","LS","LM","LL","LVL"],["VLVS","VLS","VLM","VLL","VLVL"]]
    sequence = [initial_state]
    if seed != "NA":
        np.random.seed(seed)
    for i in range(n_steps-1):
        transition_probs = transitionMatrix[states.index(sequence[-1])]
        next_state = np.random.choice(states, p=transition_probs)
        sequence.append(next_state)
    return sequence

# RANDOM SELECTION OF DURATION BASED ON LENGTHS
def get_durations(total_length, sequence, last_note_min_length=3):
    """Return list of durations for each chord in sequence."""
    length_reqd = total_length
    durations = []
    for i in range(len(sequence)):
        if sum(durations) > total_length:
            # print(durations)
            durations = durations[:-1]
            durations.append(round(total_length-sum(durations),2))
            # print(durations)
            # print(sum(durations))
            while durations[-1] < last_note_min_length:
                durations[-2] += durations[-1]
                durations=durations[:-1]
                # print(durations)
                # print(sum(durations))
            # print("exited while")
            # print(durations)
            # print(sum(durations))
            assert durations[-1] >= last_note_min_length
            assert round(sum(durations),2) == total_length
            # l = len(durations)
            return durations
            
        if i == len(sequence)-1:
            if length_reqd < last_note_min_length:
                durations.append(length_reqd)
                break
        if sequence[i] == "VS":
            durations.append(round(rm.uniform(0.5,1),2))
        elif sequence[i] == "S":
            durations.append(round(rm.uniform(1,2),2))
        elif sequence[i] == "M":
            durations.append(round(rm.uniform(2,3),2))
        elif sequence[i] == "L":
            durations.append(round(rm.uniform(3,5),2))
        elif sequence[i] == "VL":
            durations.append(round(rm.uniform(5,8),2))
        length_reqd -= durations[i]
    l = len(durations)
    assert durations[-1] >= last_note_min_length
    assert round(sum(durations),2) == total_length
    return durations

#TODO: incorporate transition matrix from one octave to another rather than random choice
def get_note_density(sequence, initial_state=3, seed="NA", transition_probs=[0.2,0.3,0.3,0.1,0.1]):
    """Return list of number of notes to be used for each chord in sequence."""
    assert sum(transition_probs) == 1
    states = [1,2,3,4,5]
    densities=[initial_state]
    for i in range(len(sequence)-1):
        densities.append(np.random.choice(states, p=transition_probs))
    return densities

#TODO: incorporate transition matrix from one octave to another rather than random choice
def get_octaves(sequence, initial_state=3, seed="NA", transition_probs=[0.3,0.5,0.1,0.1]):
    """Return list of octaves to be used for each chord in sequence."""
    assert sum(transition_probs) == 1
    octaves=[initial_state]
    for i in range(len(sequence)-1):
        octaves.append(np.random.choice([2,3,4,5], p=transition_probs))
    return octaves

def get_chord_and_metadata(total_length, ending_chord_length, length_transition_matrix, starting_chord='C', starting_length="VL", starting_density=1, starting_octave=3, seed="NA"):
    # docstring for this function
    """Create a sequence of chords and get metadata to use for synthesis ."""
    n_notes_to_generate = int(total_length/2)

    chord_sequence = generate_sequence('C', n_notes_to_generate)
    lengths = get_length_sequence(starting_length, n_notes_to_generate,length_transition_matrix, seed)
    durations = get_durations(total_length,lengths,ending_chord_length)
    chord_sequence = chord_sequence[:len(durations)]

    densities = get_note_density(chord_sequence, starting_density, seed)
    octaves = get_octaves(chord_sequence)
    print(chord_sequence)
    assert durations[-1] >= ending_chord_length
    assert round(sum(durations),2) == total_length
    return {'chords':chord_sequence, 'durations': durations, 'note_densities':densities, 'octaves':octaves}

def main(tm):
    for i in range(50):
        d=get_chord_and_metadata(500, 1, tm)
        # print(sum(d['durations']))
        print(d)
        print("-------------------------------------------------")


if __name__ == "__main__":
    transitionMatrix = np.array([
                             [0.2,0.2,0.2,0.2,0.2],
                             [0.2,0.2,0.2,0.2,0.2],
                             [0.2,0.2,0.2,0.2,0.2],
                             [0.2,0.2,0.2,0.2,0.2],
                             [0.2,0.2,0.2,0.2,0.2]
                             ])
    assert sum(transitionMatrix[0])==1
    assert sum(transitionMatrix[1])==1
    assert sum(transitionMatrix[2])==1
    assert sum(transitionMatrix[3])==1
    assert sum(transitionMatrix[4])==1
    main(transitionMatrix)