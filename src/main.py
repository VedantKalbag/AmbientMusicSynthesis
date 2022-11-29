import os
import json
import numpy as np
import synth
import gensound
from gensound.signals import Sine, Sawtooth, Square, Triangle, WhiteNoise, Silence, PinkNoise, Mix, WAV
from gensound.effects import OneImpulseReverb, Vibrato
from gensound.filters import SimpleBandPass, SimpleHPF, SimpleLPF, SimpleHighShelf, SimpleLowShelf
from gensound.transforms import ADSR, Fade, Amplitude, CrossFade
from gensound.curve import SineCurve, Line

import musical_params_unified as musical_params


from icecream import ic
ic.configureOutput(prefix='Debug | ')#, includeContext=True)
ic.disable()
class AmbientMusicSynthesis():
    def __init__(self):
        # print(os.path.join(os.path.dirname(__file__),'..','presets','themes', 'musical_params.json'))
        self.themes = json.load(open(os.path.join(os.path.dirname(__file__),'..','presets', 'themes.json')))
        self.musical_params = json.load(open(os.path.join(os.path.dirname(__file__),'..','presets', 'musical_params.json')))
        self.timbral_params = json.load(open(os.path.join(os.path.dirname(__file__),'..','presets', 'timbre.json')))
    def interpolate_parameter(self, initial, final, num_steps, integer_output=False):
        """
        Interpolates between two values
        """
        if integer_output:
            return np.linspace(initial, final, num_steps, dtype=int)
        if type(initial) == str:
            return np.array([initial if i <= num_steps/2 else final for i in range(num_steps)])
        return np.linspace(initial, final, num_steps)
    def generate_audio(self,desired_duration, emotion_timestamp_dict, sample_rate, theme='default'):
        """
        Generate audio based on user input.
        @param: duration The desired total duration of the audio in seconds.
        @param: emotion_timestamp_dict a dictionary containing keys as timestamps and values as emotion at the timestamp.
        @param: theme The theme for audio generation
        """
        # get user input
        # get theme
        self._theme = self.themes[theme]
        # get musical parameters
        self._musical_params = self.musical_params[self._theme['musical_params']]
        # get timbral parameters
        self._timbral_params = self.timbral_params[self._theme['timbral_params']]

        starting_key = np.random.choice(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])
        starting_note_density = np.random.choice([1,2,3,4,5])
        starting_length = np.random.choice(["VS", "S", "M", "L", "VL"])

        self.mp = musical_params.MusicalParameters(
                                duration=desired_duration, 
                                ending_chord_min_length=2, 
                                starting_key=starting_key, 
                                starting_length=starting_length, 
                                starting_note_density=starting_note_density, 
                                starting_octave=4, 
                                preset_dict = self.musical_params)
        d = self.mp.get_musical_parameters(emotion_timestamp_dict)
        chords, durations = d['chords'], d['durations']
        ic(len(chords))
        ic(len(durations))
        ic(sum(durations))
        
        # print(end)
        # interpolates between the consecutive parameters 
        # use the number of steps between the emotions for interpolation
        keys = list(emotion_timestamp_dict.keys())
        values = list(emotion_timestamp_dict.values())
        emotion_intervals = {}
        for i in range(len(emotion_timestamp_dict.keys())-1):
            emotion_intervals[(keys[i], keys[i+1])] = (values[i], values[i+1])
        if keys[i+1] < desired_duration:
            # emotion_intervals.append((list(mood_map.keys())[i+1], desired_duration))
            emotion_intervals[(keys[i+1], desired_duration)] = (values[i+1], values[i+1])

        #  create a dict of lists of timbral parameters, interpolating between the different emotion segments
        t_params = {}
        k = list(emotion_intervals.keys())
        # print(k[0])
        v = list(emotion_intervals.values())
        steps={}
        start = 0
        end = 0
        for interval in k:
            while sum(durations[start:end]) < (interval[1] - interval[0]):
                end += 1
                if end > len(durations):
                    break
            steps[interval] = end - start # FIXME: This value is occasionally higher than the true number by 1
            duration = list(interval)[1] - list(interval)[0]
            ic(f"{start} - {end} - {steps[interval]} - {sum(durations[start:end])} - {duration}")
            start = end
            for param in self.timbral_params['default'].keys():
                initial_param_value = self.timbral_params[str(emotion_intervals[interval][0])][param]
                final_param_value = self.timbral_params[str(emotion_intervals[interval][1])][param]
                if (param != 'automation') and (param.find('noise') == -1):
                    if param != 'n_voices':
                        if interval == k[0]: # for first interval
                            t_params[param] = self.interpolate_parameter(initial_param_value, final_param_value, steps[interval])
                        else:
                            t_params[param] = np.concatenate((t_params[param], self.interpolate_parameter(initial_param_value, final_param_value, steps[interval])))
                    else:
                        if interval == k[0]:
                            t_params[param] = self.interpolate_parameter(initial_param_value, final_param_value, steps[interval], integer_output=True)
                        else:
                            t_params[param] = np.concatenate((t_params[param], self.interpolate_parameter(initial_param_value, final_param_value, steps[interval], integer_output=True)))
                elif (param.find('noise') != -1):
                    # print(steps[interval])
                    if interval == k[0]:
                        t_params[param] = self.interpolate_parameter(initial_param_value, final_param_value, steps[interval])
                    else:
                        t_params[param] = np.concatenate((t_params[param], self.interpolate_parameter(initial_param_value, final_param_value, steps[interval])))
                    # print(len(t_params[param]))
        # ic(t_params)
        # print(len(t_params[list(t_params.keys())[0]]))
        # # DEBUGGING ONLY:
        # for param in t_params.keys():
        #     print(param, len(t_params[param]))

        # GENERATE AUDIO
        ic("length of chords: ", len(chords))
        ic("length of durations: ", len(durations))
        ic(t_params[list(t_params.keys())[0]])
        ic(len(t_params[list(t_params.keys())[0]]))
        for i in range(len(t_params[list(t_params.keys())[0]])):
            # print(i)
            params={}
            for param in t_params.keys():
                # print(param,len(t_params[param]))
                params[param] = t_params[param][i]
            # print(params)
            self.s = synth.Synth(params) # TODO: OPTIMISE BY CHECKING IF PARAMS ARE SAME AS PREVIOUS ITERATION
            for i in range(len(chords)):
                if i == 0:
                    self.audio = gensound.mix([self.s.generate_audio(midi, durations[i]*1e3) for midi in chords[i]])
                else:
                    self.audio = self.audio | CrossFade(duration=0.5*1e3) | gensound.mix([self.s.generate_audio(midi, durations[i]*1e3) for midi in chords[i]])
            # if i == 0:
            #     ic(chords[i])
            #     audio = gensound.mix([self.s.generate_audio(midi, durations[i]) for midi in chords[i]])
            #     # audio=Silence(durations[i])
            #     # for midi in chords[i]:
            #     #     audio = gensound.mix([self.s.generate_audio(m,durations[i]) for m in ])#gensound.mix([self.s.generate_audio(midi, durations[i]*1e3), audio])
            #     # audio = self.s.generate_audio(chords[i], durations[i]*1e3)
            # else:
            #     # tmp = gensound.mix([self.s.generate_audio(midi, durations[i]) for midi in chords[i]])
            #     # tmp=Silence(durations[i])
            #     # for midi in chords[i]:
            #     #     tmp = gensound.mix([self.s.generate_audio(midi, durations[i]*1e3), tmp])
            #     # tmp = self.s.generate_audio(chords[i], durations[i]*1e3)
            #     ic(chords[i])
            #     audio = audio | gensound.mix([self.s.generate_audio(midi, durations[i]) for midi in chords[i]])#self.s.generate_audio(chords[i], durations[i]*1e3)
        return self.audio#.realise(sample_rate)
    def export_audio(self, filename,audio=''):
        if audio == '':
            self.audio.export(f"{filename}")
        else:
            audio.export(filename)
if __name__ == "__main__":
    import timeit
    starttime = timeit.default_timer()
    ams = AmbientMusicSynthesis()
    audio = ams.generate_audio(90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, sample_rate=44100)
    # print(audio)
    # print(audio.realise(44100))
    # audio.play()
    ams.export_audio('test_2.wav')
    print("The time taken is :", timeit.default_timer() - starttime)