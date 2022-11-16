import numpy as np
import random as rm
# note_durations = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
# The statespace
states = ["VS","S","M","L","VL"]
# Possible sequences of events
transitionName = [["VSVS","VSS","VSM","VSL","VSVL"],["SVS","SS","SM","SL","SVL"],["MVS","MS","MM","ML","MVL"],["LVS","LS","LM","LL","LVL"],["VLVS","VLS","VLM","VLL","VLVL"]]

# Probabilities matrix (transition matrix)
#TODO: Load transition matrix, last_note_min_length from each theme
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


def get_length_sequence(initial_state, n_steps, seed="NA"):
    sequence = [initial_state]
    if seed != "NA":
        np.random.seed(seed)
    for i in range(n_steps-1):
        transition_probs = transitionMatrix[states.index(sequence[-1])]
        next_state = np.random.choice(states, p=transition_probs)
        sequence.append(next_state)
    return sequence

def get_durations(total_length, sequence, last_note_min_length=3):
    length_reqd = total_length
    durations = []
    for i in range(len(sequence)):
        if sum(durations) > total_length:
            durations = durations[:-1]
            durations.append(round(total_length-sum(durations),2))
            if durations[-1] < last_note_min_length:
                durations[-2] += durations[-1]
                durations=durations[:-1]
            assert durations[-1] >= last_note_min_length
            assert sum(durations) == total_length
            l = len(durations)
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
    assert sum(durations) == total_length
    return durations

def main():
    for i in range(20):
        print(get_durations(20,get_length_sequence("VL",20),2))

if __name__ == "__main__":
    main()