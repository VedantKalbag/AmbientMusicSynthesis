import os
from icecream import ic
ic.configureOutput(prefix='Debug | ')#, includeContext=True)
# ic.disable()
import numpy as np
import pandas as pd
import random as rm
from collections import OrderedDict

class MusicalParameters():
    def __init__(self, duration, ending_chord_min_length, starting_key, starting_length, starting_note_density, starting_octave, preset_dict):
        self.__dict__ = preset_dict['default'] # initialize based on first emotion segment 
        self.preset_dict = preset_dict
        self.preset_keys = list(preset_dict.keys())
        # ic(self.preset_dict)
        # self.composition_probabilities, self.key_type  to be included in preset dict, will change from one theme to another

        self.desired_duration = duration
        self.ending_chord_min_length = ending_chord_min_length
        self.current_key = starting_key
        self.current_length = starting_length
        self.current_note_density = starting_note_density
        self.current_octave = starting_octave
        
        self.current_chord=None

        if self.current_length == "VS":
            self.current_duration = round(rm.uniform(0.5,1),2)
        elif self.current_length == "S":
            self.current_duration = round(rm.uniform(1,2),2)
        elif self.current_length == "M":
            self.current_duration = round(rm.uniform(2,3),2)
        elif self.current_length == "L":
            self.current_duration = round(rm.uniform(3,5),2)
        elif self.current_length == "VL":
            self.current_duration = round(rm.uniform(5,8),2)

        self.major_key_transitions = OrderedDict({
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
        self.minor_key_transitions = OrderedDict({
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
        self.key_transition_probability = np.array([0.3,0.3,0.3,0.1])
        
        self.NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        
        self.OCTAVES=list(range(11))
        self.NOTES_IN_OCTAVE = len(self.NOTES)
        
        self.length_states = ["VS","S","M","L","VL"]

    def get_major_scale(self,midi_note):
        return [midi_note, midi_note + 2, midi_note + 4, midi_note + 5, midi_note + 7, midi_note + 9, midi_note + 11, midi_note + 12]

    def get_minor_scale(self,midi_note):
        return [midi_note, midi_note + 2, midi_note + 3, midi_note + 5, midi_note + 7, midi_note + 8, midi_note + 10, midi_note + 12]

    def get_roots_search_space(self,midi_note):
        major_scale = self.get_major_scale(midi_note)
        # print (major_scale)
        minor_scale = self.get_minor_scale(midi_note)
        # print(minor_scale)
        major_roots = np.array([major_scale[3-1], major_scale[-3]-12])
        # print (major_roots)
        minor_roots = np.array([minor_scale[3-1], minor_scale[-3]-12])
        # print(minor_roots)
        return np.append(major_roots, minor_roots)

    def get_major_intervals(self,num_notes):
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

    def get_minor_intervals(self,num_notes):
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

    def get_chord_search_space(self,midi_note, num_notes=3):
        roots = self.get_roots_search_space(midi_note)
        major_interval = self.get_major_intervals(num_notes)
        minor_interval = self.get_minor_intervals(num_notes)
        major_chords = []
        minor_chords = []
        for root in roots:
            major_chords.append(root + major_interval)
            minor_chords.append(root + minor_interval)
        return np.append(major_chords, minor_chords, axis=0)

    def number_to_note(self, number: int) -> tuple:
        octave = number // self.NOTES_IN_OCTAVE
        # assert octave in OCTAVES
        # assert 0 <= number <= 127
        note = self.NOTES[number % self.NOTES_IN_OCTAVE]

        return number % self.NOTES_IN_OCTAVE, note, octave # Note number (0-11), note name, octave

    def note_to_number(self,note: str, octave: int) -> int:
        assert note in self.NOTES
        # assert octave in OCTAVES

        note = self.NOTES.index(note)
        note += (self.NOTES_IN_OCTAVE * octave)

        # assert 0 <= note <= 127

        return note

    def flatten(self,l):
        return [item for sublist in l for item in sublist]

    def get_next_length(self, current_state, transition_matrix):
        return np.random.choice(self.length_states, p=transition_matrix[self.length_states.index(current_state)])
    
    # TODO: the case for last chord length needs to be handled in the wrapper function   
    def get_next_duration(self, current_duration, transition_matrix): 
        # ic(current_duration)
        if current_duration < 1:
            current_length = "VS"
        elif 1 <= current_duration < 2:
            current_length = "S"
        elif 2 <= current_duration < 3:
            current_length = "M"
        elif 3 <= current_duration < 5:
            current_length = "L"
        elif 5 <= current_duration <= 8:
            current_length = "VL"
        # ic(current_length)
        next_length = self.get_next_length(current_length, transition_matrix)

        assert next_length in ["VS","S","M","L","VL"]
        match next_length:
            case "VS":
                return round(rm.uniform(0.5,1),2)
            case "S":
                return round(rm.uniform(1,2),2)
            case "M":
                return round(rm.uniform(2,3),2)
            case "L":
                return round(rm.uniform(3,5),2)
            case "VL":
                return round(rm.uniform(5,8),2)

    def get_next_num_notes(self, current_num_notes, num_notes_transition_matrix):
        return np.random.choice([1,2,3,4,5], p=num_notes_transition_matrix[current_num_notes-1])
    
    def get_next_octave(self, current_octave, octave_transition_matrix):
        return np.random.choice([2,3,4,5], p=octave_transition_matrix[current_octave-2])
    
    def get_nearest_chord(self,current_chord):
        # ic(current_chord)
        sorted_current_chord=sorted([self.number_to_note(note)[0] for note in current_chord])
        possible_chords=[]
        nearest_chords=[]
        chords_midi=self.get_chord_search_space(current_chord[0])
        # ic(len(current_chord), self.current_note_density)
        if len(sorted_current_chord) != self.current_note_density:
            # ic("Length mismatch")
            match self.key_type:
                case "major":
                    # ic("Major root: ", current_chord[0] + self.get_major_intervals(self.current_note_density))
                    return current_chord[0] + self.get_major_intervals(self.current_note_density), np.array(current_chord[0] + self.get_major_intervals(self.current_note_density))
                case "minor":
                    # ic("Minor root: ",current_chord[0] + self.get_minor_intervals(self.current_note_density))
                    return current_chord[0] + self.get_minor_intervals(self.current_note_density), np.array(current_chord[0] + self.get_minor_intervals(self.current_note_density))
        
        for chord in self.get_chord_search_space(current_chord[0]):
            possible_chords.append([self.number_to_note(note)[0] for note in chord])
            for i in range(len(current_chord)):
                # ic(np.array([self.number_to_note(note)[0] for note in chord]))
                # ic(sorted_current_chord)
                try:
                    mask = np.count_nonzero(np.roll(np.array([self.number_to_note(note)[0] for note in chord]),i) - sorted_current_chord) == 1
                    if np.all(mask) != False:
                        # print(chord)
                        nearest_chords.append(chord)
                except:
                    pass
        # ic(nearest_chords)
        if nearest_chords == []:
            # ic("No nearest chord found")
            # ic(self.key_type)
            # ic(self.current_key[:1])
            # ic(self.note_to_number(self.current_key[:1],self.current_octave))
            match self.key_type:
                case 'major':
                    # ic(self.note_to_number(self.current_key,self.current_octave) + self.get_major_intervals(len(current_chord)))
                    nearest_chords.append(self.note_to_number(self.current_key[:1],self.current_octave) + self.get_major_intervals(len(current_chord)))
                case 'minor':
                    # ic(self.note_to_number(self.current_key,self.current_octave) + self.get_minor_intervals(len(current_chord)))
                    nearest_chords.append(self.note_to_number(self.current_key[:1],self.current_octave) + self.get_minor_intervals(len(current_chord)))
        ic(nearest_chords)
        return rm.choice(nearest_chords), np.array(nearest_chords)

    def key_change(self, current_chord, key_type):
        sorted_current_chord=sorted([self.number_to_note(note)[0] for note in current_chord])
        # ic(self.major_key_transitions[self.current_key])
        # ic(self.minor_key_transitions[self.current_key])
        # Choose new key
        if self.current_key in list(self.major_key_transitions.keys())[:12]:
            new_key = np.random.choice(self.major_key_transitions[self.current_key], p=self.key_transition_probability)
            while (new_key == self.current_key):
                new_key = np.random.choice(self.major_key_transitions[self.current_key], p=self.key_transition_probability)
            self.current_key = new_key
        elif self.current_key in list(self.minor_key_transitions.keys())[:12]:
            new_key = np.random.choice(self.minor_key_transitions[self.current_key], p=self.key_transition_probability)
            while (new_key == self.current_key):
                new_key = np.random.choice(self.minor_key_transitions[self.current_key], p=self.key_transition_probability)
            self.current_key = new_key
        else:
            ic("Current Key not found in major or minor key transitions")
        # TODO: get the 5 and root of the new key instead of finding nearest chord
        # Currently system will play just the root of the new key
        # ic(new_key)
        new_key_root_midi = self.note_to_number(self.current_key[:1],self.current_octave)#self.note_to_number(new_key[:1], self.current_octave)
        if key_type == "major":
            chord = new_key_root_midi + self.get_major_intervals(self.current_note_density)
        elif key_type == "minor":
            chord = new_key_root_midi + self.get_minor_intervals(self.current_note_density)
        
        # # Get new chord
        # _, nearest_chords = self.get_nearest_chord(current_chord)
        # if key_type == 'major':
        #     for c in nearest_chords:
        #         # check if chord c exists in the scale of the new key
        #         if c[0] in self.major_scales[self.current_key]:
        #             chord = c
        #             break
        # elif key_type == 'minor':
        #     for c in nearest_chords:
        #         # check if chord c exists in the scale of the new key
        #         if c[0] in self.minor_scales[self.current_key]:
        #             chord = c
        #             break
        return chord
    
    def _update_musical_parameters(self, emotion_segment):
        # TODO: create these parameter dicts
        # ic(self.__dict__)
        match emotion_segment:
            # load from musical parameters json
            case 1:
                # ic(self.preset_dict["1"])
                # self.__dict__ = self.preset_dict["1"]
                for key in self.preset_dict["1"].keys():
                    self.__dict__[key] = self.preset_dict["1"][key]
                # self.__dict__ = {
                #     "composition_probabilities" : np.array([]),
                #     "key_transition_probability" : np.array([]),
                #     "key_type" : "",
                #     "note_density_transition_matrix" : np.array([]),
                #     "octave_transition_matrix" : np.array([])
                # }
            case 2:
                # ic(self.preset_dict["2"])
                # self.__dict__ = self.preset_dict["2"]
                for key in self.preset_dict["2"].keys():
                    self.__dict__[key] = self.preset_dict["2"][key]
                # self.__dict__ = {
                #     "composition_probabilities" : np.array([]),
                #     "key_transition_probability" : np.array([]),
                #     "key_type" : "",
                #     "note_density_transition_matrix" : np.array([]),
                #     "octave_transition_matrix" : np.array([])
                # }
            case 3:
                # ic(self.preset_dict["3"])
                # self.__dict__ = self.preset_dict["3"]
                for key in self.preset_dict["3"].keys():
                    self.__dict__[key] = self.preset_dict["3"][key]
                # self.__dict__ = {
                #     "composition_probabilities" : np.array([]),
                #     "key_transition_probability" : np.array([]),
                #     "key_type" : "",
                #     "note_density_transition_matrix" : np.array([]),
                #     "octave_transition_matrix" : np.array([])
                # }
            case 4:
                # ic(self.preset_dict["4"])
                # self.__dict__ = self.preset_dict["4"]
                for key in self.preset_dict["4"].keys():
                    self.__dict__[key] = self.preset_dict["4"][key]
                # self.__dict__ = {
                #     "composition_probabilities" : np.array([]),
                #     "key_transition_probability" : np.array([]),
                #     "key_type" : "",
                #     "note_density_transition_matrix" : np.array([]),
                #     "octave_transition_matrix" : np.array([])
                # }
            case 5:
                # ic(self.preset_dict["5"])
                # self.__dict__ = self.preset_dict["5"]
                for key in self.preset_dict["5"].keys():
                    self.__dict__[key] = self.preset_dict["5"][key]
                # self.__dict__ = {
                #     "composition_probabilities" : np.array([]),
                #     "key_transition_probability" : np.array([]),
                #     "key_type" : "",
                #     "note_density_transition_matrix" : np.array([]),
                #     "octave_transition_matrix" : np.array([])
                # }
        return

    def get_musical_parameters(self, mood_map={}):
        assert len(list(mood_map.keys())) >= 2, "Mood map should contain at least two timestamps and emotion segments"
        assert int(list(mood_map.keys())[0]) == 0, "Mood map should start at 0 seconds"
        assert int(list(mood_map.keys())[-1]) == self.desired_duration, "Mood map should end at the duration of the composition"
        
        # print(mood_map[list(mood_map.keys())[0]])
        self._update_musical_parameters(mood_map[list(mood_map.keys())[0]])

        emotion_time_intervals = []
        l = list(mood_map.keys())
        for i in range(len(l)-1):
            emotion_time_intervals.append((l[i], l[i+1]))
        if l[i+1] < self.desired_duration:
            emotion_time_intervals.append((l[i+1], self.desired_duration))

        chords=[]
        durations=[]
        for idx, time_interval in enumerate(emotion_time_intervals):
            ic(time_interval)
            # TODO
            # Repeat while length of the generated sequence is less than the desired length
            # 1. get next chord length and duration
            # 2. get next number of notes
            # 3. get next octave
            # 4. get next chord
            # if total_length > desired length, increase the previous note by the difference
            # while the last chord length < self.ending_chord_min_length, combine the last two durations
            # select chords = chords[:len(durations)]
            # return chords, durations

            time_interval_duration = time_interval[1] - time_interval[0]
            time_interval_chords = []
            time_interval_durations = []

            # ic(self.__dict__)
            # ic(self.desired_duration)
            while sum(time_interval_durations) < time_interval_duration:#self.desired_duration:
                next_chord_duration = self.get_next_duration(self.current_duration, self.duration_transition_matrix)
                num_notes = self.get_next_num_notes(self.current_note_density, self.note_density_transition_matrix)
                octave = self.get_next_octave(self.current_octave, self.octave_transition_matrix)

                composition_type = rm.choices(['nearest','circle_of_fifths'], weights=self.composition_probabilities)[0]
                # ic(composition_type)
                # ic(composition_type == 'nearest')
                # ic(composition_type == 'circle_of_fifths')
                #TODO: Get nearest chord based on whether to use nearest chords or key change
                if self.current_chord is not None:
                    # if using nearest chords, get nearest chord
                    if composition_type == 'nearest':
                        # ic('Using nearest chord method')
                        # ic("Current chord: ", self.current_chord)
                        next_chord, nearest_chords = self.get_nearest_chord(self.current_chord)
                        # ic(next_chord)
                    # if using key change, get nearest chord in the new key by finding the new key from the circle of fifths 
                    # and evaluating the chord search space to find the nearest one
                    elif composition_type == 'circle_of_fifths':
                        # ic('Using circle of fifths')
                        next_chord = self.key_change(self.current_chord, self.key_type) 
                        # ic(next_chord)
                else:
                    new_key_root_midi = self.note_to_number(self.current_key, self.current_octave)
                    if self.key_type == "major":
                        next_chord = new_key_root_midi + self.get_major_intervals(self.current_note_density)
                    elif self.key_type == "minor":
                        next_chord = new_key_root_midi + self.get_minor_intervals(self.current_note_density)

                # ic(next_chord)
                # UPDATE CURRENT VALUES:
                # self._update(next_chord_duration, num_notes, octave, next_chord, nearest_chords, key_type)
                time_interval_durations.append(next_chord_duration)
                time_interval_chords.append(next_chord)
                # MUSICAL PARAMETER UPDATE BASED ON MOOD MAP:
                # if current time (calculated by sum of durations) is in range(time_interval[1] - time_interval[0]) then find the segment associated with time_interval[1]
                # if current time is more than halfway through the range, perform musical parameter update
                current_time = sum(time_interval_durations)
                if current_time > time_interval[0] + 0.66*(time_interval_duration):
                    try:
                        next_emotion_segment = mood_map[time_interval[1]]
                    except:
                        next_emotion_segment = mood_map[time_interval[0]]
                    ic(next_emotion_segment)
                    self._update_musical_parameters(next_emotion_segment)

                self.current_duration = next_chord_duration
                self.current_note_density = num_notes
                self.current_octave = octave
                self.current_chord = next_chord
            ic("------------------------------------------")
            ic(len(time_interval_chords))
            ic(len(time_interval_durations))
            # processing to cut the last note to meet the interval duration
            if sum(time_interval_durations) > time_interval_duration:
                time_interval_durations[-1] = time_interval_durations[-1] - (sum(time_interval_durations) - time_interval_duration)

            # Handling the case where the last note minimum duration is not met
            if sum(durations) > self.desired_duration: 
                durations = durations[:-1]
                durations.append(round(self.desired_duration-sum(durations),2))
                while durations[-1] < self.ending_chord_min_length:
                    durations[-2] += durations[-1]
                    durations=durations[:-1]
                assert durations[-1] >= self.ending_chord_min_length
                assert round(sum(durations),2) == self.desired_duration
            # ic(sum(time_interval_durations))
            
            # time_interval_chords = time_interval_chords[:len(durations)] # FIXME: This line isn't ensuring the lists are of the same length
            ic(len(time_interval_durations) == len(time_interval_chords))
            ic(len(time_interval_chords))
            ic(len(time_interval_durations))
            # TODO: Consider scanning the end of the chord sequence and change the last chord to include a resolution
            chords.extend(time_interval_chords)
            durations.extend(time_interval_durations)
            ic(len(chords))
            ic(len(durations))
        ic(len(chords))
        ic(len(durations))
        assert len(chords) == len(durations)
        return {"chords": chords, "durations": durations}


if __name__ == "__main__":
    mp = MusicalParameters(
                        duration=90, 
                        ending_chord_min_length=2, 
                        starting_key='C', 
                        starting_length="VL", 
                        starting_note_density=3, 
                        starting_octave=4, 
                        preset_dict = {
                            "default":
                                {
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                },
                            "1": 
                            {
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                },
                            "2":
                            {
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                },
                            "3":{
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                },
                            "4":{
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                },
                            "5":
                            {
                                    "composition_probabilities":[0.5,0.5], 
                                    "key_transition_probability":[0.3,0.3,0.3,0.1], 
                                    "key_type":'major', 
                                    "note_density_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]]), 
                                    "octave_transition_matrix":np.array([[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25],[0.25,0.25,0.25,0.25]]), 
                                    "duration_transition_matrix":np.array([[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2],[0.2,0.2,0.2,0.2,0.2]])
                                }
                                    }
                            )
    print(mp.get_musical_parameters(mood_map={0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1})) # TODO: there are no clean endpoints for the end of each section in terms of durations
    # import timeit
    # print(timeit.timeit("""[mp.get_musical_parameters(mood_map={0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}) for i in range(500)]""", setup="from __main__ import mp", number=1))