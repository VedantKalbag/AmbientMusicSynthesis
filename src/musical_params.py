import numpy as np
import pandas as pd
import random as rm

from collections import Counter
# np.random.seed(42)

import os
print(os.getcwd())



# MARKOV CHAIN FOR CHORDS
# ----------------------------------------------------------------------
def predict_next_state(chord:str, segment:int=1):
    """Predict next chord based on current state."""
        # read file
    data = pd.read_csv('resources/Liverpool_band_chord_sequence.csv')
    # ----------------------------------------------------------------------
    n = 3
    chords = data['chords'].values
    ngrams = zip(*[chords[i:] for i in range(n)])
    bigrams = [" ".join(ngram) for ngram in ngrams]
    # create list of bigrams which stats with current chord
    bigrams_with_current_chord = [bigram for bigram in bigrams if bigram.split(' ')[0]==chord]
    # count appearance of each bigram
    count_appearance = dict(Counter(bigrams_with_current_chord))
    # convert apperance into probabilities
    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram]/len(bigrams_with_current_chord)
    
    # create list of possible options for the next chord
    options = [key.split(' ')[1] for key in count_appearance.keys()]
    # print(options)
    # create  list of probability distribution
    probabilities = list(count_appearance.values())
    # return random prediction
    return np.random.choice(options, p=probabilities)

# ----------------------------------------------------------------------
def generate_sequence(chord:str=None, length:int=30):
    """Generate sequence of defined length."""
    # create list to store future chords
    chords = []
    chords.append(chord)
    for n in range(length-1):
        # append next chord for the list
        chords.append(predict_next_state(chord))
        # use last chord in sequence to predict next chord
        chord = chords[-1]
    return chords


# MARKOV CHAIN FOR CHORD LENGTHS
def get_length_sequence(initial_state, n_steps,transitionMatrix, seed="NA"):
    """Return sequence of chord lengths based on initial state and transition matrix."""
    # The statespace
    states = ["VS","S","M","L","VL"]
    # Possible sequences of events
    transitionName = [["VSVS","VSS","VSM","VSL","VSVL"],["SVS","SS","SM","SL","SVL"],["MVS","MS","MM","ML","MVL"],["LVS","LS","LM","LL","LVL"],["VLVS","VLS","VLM","VLL","VLVL"]]
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
            print(durations)
            print(sum(durations))
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

def get_note_density(sequence, initial_state=3, seed="NA", transition_probs=[0.2,0.3,0.3,0.1,0.1]):
    """Return list of number of notes to be used for each chord in sequence."""
    assert sum(transition_probs) == 1
    states = [1,2,3,4,5]
    densities=[initial_state]
    for i in range(len(sequence)-1):
        densities.append(np.random.choice(states, p=transition_probs))
    return densities

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
    n_notes_to_generate = int(total_length/1)

    chord_sequence = generate_sequence('C', n_notes_to_generate)
    lengths = get_length_sequence(starting_length, n_notes_to_generate,length_transition_matrix, seed)
    durations = get_durations(total_length,lengths,ending_chord_length)
    chord_sequence = chord_sequence[:len(durations)]

    densities = get_note_density(chord_sequence, starting_density, seed)
    octaves = get_octaves(chord_sequence)

    assert durations[-1] >= ending_chord_length
    assert round(sum(durations),2) == total_length
    return {'chords':chord_sequence, 'durations': durations, 'note_densities':densities, 'octaves':octaves}

def main(tm):
    for i in range(50):
        d=get_chord_and_metadata(360, 1, tm)
        # print(sum(d['durations']))
        # print(d)
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