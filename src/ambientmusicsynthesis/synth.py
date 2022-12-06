import os
import gensound
from gensound.signals import Sine, Sawtooth, Square, Triangle, WhiteNoise, Silence, PinkNoise, Mix, WAV
from gensound.effects import OneImpulseReverb, Vibrato
from gensound.filters import SimpleBandPass, SimpleHPF, SimpleLPF, SimpleHighShelf, SimpleLowShelf
from gensound.transforms import ADSR, Fade, Amplitude, CrossFade
from gensound.curve import SineCurve, Constant, Line

from icecream import ic
ic.configureOutput(prefix='Debug | ')


class Synth():
    def __init__(self, params):
        # self.preset = preset
        # if self.preset == 'default':
            # load json file containing default settings
        # data = json.load(open(os.path.join(path_to_preset,'timbre.json')))[self.preset]
        # data = mellow_o
        # print(data)
        self.__dict__ = params#data
        self.NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        self.OCTAVES=list(range(11))
        self.NOTES_IN_OCTAVE = len(self.NOTES)
        self.NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.filters={}
        for filter_number in ['filter1','filter2','filter3']:
            if self.__dict__[filter_number+'_type'] == 'na':
                self.__dict__[filter_number] = None
            else:
                match self.__dict__[filter_number+'_type']:
                    case 'lowpass':
                        self.__dict__[filter_number] = SimpleLPF
                    case 'highpass':
                        self.__dict__[filter_number] = SimpleHPF
                    case 'bandpass':
                        self.__dict__[filter_number] = SimpleBandPass
                    case 'lowshelf':
                        self.__dict__[filter_number] = SimpleLowShelf
                    case 'highshelf':
                        self.__dict__[filter_number] = SimpleHighShelf
                # self.__dict__[filter_number] = f(self.__dict__[filter_number+'_freq'])
    # def _setparam(self, param, value):
    #     setattr(self, param, value)
    def midi_to_freq(self, midi_number):
        return 440 * 2**((midi_number-69)/12)
    def shift_freq_by_cents(self, freq, cents):
        return freq*(10**(cents/(1200*3.322038403)))
    def semitones_to_cents(self, semitones):
        return semitones*100
    def cents_to_semitones(self, cents):
        return cents/100
    def octave_to_multiplier(self, octave):
        return 2**(octave)
    # def NoteToMidi(self, KeyOctave):
    #     # KeyOctave is formatted like 'C#3'
    #     key = KeyOctave[:-1]  # eg C, Db
    #     octave = KeyOctave[-1]   # eg 3, 4
    #     answer = -1

    #     try:
    #         if 'b' in key:
    #             pos = self.NOTES_FLAT.index(key)
    #         else:
    #             pos = self.NOTES_SHARP.index(key)
    #     except:
    #         print('The key is not valid', key)
    #         return answer

    #     answer += pos + 12 * (int(octave) + 1) + 1
    #     return answer
    # def number_to_note(self, number: int) -> tuple:
    #     octave = number // self.NOTES_IN_OCTAVE
    #     # assert octave in OCTAVES
    #     # assert 0 <= number <= 127
    #     note = self.NOTES[number % self.NOTES_IN_OCTAVE]
    #     return number % self.NOTES_IN_OCTAVE, note, octave # Note number (0-11), note name, octave

    # def note_to_number(self,note: str, octave: int) -> int:
    #     assert note in self.NOTES
    #     # assert octave in OCTAVES
    #     note = self.NOTES.index(note)
    #     note += (self.NOTES_IN_OCTAVE * octave)
    #     # assert 0 <= note <= 127
    #     return note

    def detuned_voices(self, midi_number, relative_shift, duration, detune_pct, n_voices, wave_type='square'): # TODO: Change pitch to midi number
        # n_voices = how many oscillators in the array
        # detune_range = the difference in cents between the highest and lowest oscillators in the array

        freq = self.midi_to_freq(midi_number)#self.pitch_to_freq(self.NoteToMidi(pitch))
        # ic(freq)
        detune_range = freq * int(detune_pct)/100
        all_cents = [i*detune_range/n_voices - detune_range/2 for i in range(n_voices)] # how much to detune each signal in the array
        # print(isinstance(pitch, str))
        match wave_type: # REQUIRES PYTHON 3.10
            case 'sine':
                f = Sine
            case 'square':
                f = Square
            case 'triangle':
                f = Triangle
            case 'sawtooth':
                f = Sawtooth
        return gensound.mix([f(self.shift_freq_by_cents(freq*relative_shift,cents),duration) for cents in all_cents])
    
    def generate_audio(self, midi_number,duration): # TODO: change pitch to midi number
        # 2 LFOS for amplitude modulation
        # if self.lfo1_type != 'na':
        #     self.lfo1 = Amplitude(SineCurve(frequency=self.lfo1_freq, depth=self.lfo1_depth, baseline=0.5, duration=duration))
        # else:
        #     self.lfo1 = Amplitude(Constant(1, duration=duration))
        # if self.lfo2_type != 'na':
        #     self.lfo2 = Amplitude(SineCurve(frequency=self.lfo2_freq, depth=self.lfo2_depth, baseline=0.5, duration=duration))
        # else:
        #     self.lfo2 = Amplitude(Constant(1, duration=duration))

        # 2 oscillators for the main sound
        self.osc1 = self.detuned_voices(midi_number, relative_shift=0, duration=duration,detune_pct = self.osc1_detune, n_voices = self.n_voices, wave_type=self.osc1_wave)
        self.osc2 = self.detuned_voices(midi_number, relative_shift=self.osc2_relative_shift, duration=duration,detune_pct = self.osc2_detune, n_voices = self.n_voices, wave_type=self.osc2_wave)
        # 1 oscillator for the sub bass
        if self.sub_freq != 0:
            self.sub_bass = self.detuned_voices(self.sub_freq, relative_shift=1, duration=duration,detune_pct = self.sub_detune, n_voices = self.n_voices, wave_type='sine')
        else:
            self.sub_bass = Silence(duration=duration)
        
        # 1 oscillator for the high frequency noise
        if self.hf_noise_type != 'na':
            self.high_freq_noise = WhiteNoise(duration=duration)
        else:
            self.high_freq_noise = Silence(duration=duration)
        # 1 oscillator for the low frequency noise
        if self.lf_noise_type != 'na':
            self.low_freq_noise = PinkNoise(duration=duration)
        else:
            self.low_freq_noise = Silence(duration=duration)
        
        # Filters
        # if self.filters['filter1'] is not None:
        #     self.filter1 = self.filters['filter1'](self.filter1_freq)
        # else:
        #     self.filter1 = None
        # if self.filters['filter2'] is not None:
        #     self.filter2 = self.filters['filter2'](self.filter2_freq)
        # else:
        #     self.filter2 = None
        
        # apply lfo1 and lfo2 to osc1 and osc2 amplitude
        # if self.lfo1_freq != 0:
        #     self.lfo1 = self.osc1 * self.lfo1
        # if self.lfo2_freq != 0:
        #     self.lfo2 = self.osc2 * self.lfo2
        self.output = self.osc1 + self.osc2 #+ self.sub_bass + self.high_freq_noise + self.low_freq_noise
        # if duration < 2:
        #     self.output = self.output * Fade(is_in=True,duration=duration*1000/2)
        #     self.output = self.output * Fade(is_in=False,duration=duration*1000/2)
        # else:
        #     self.output *= Fade(is_in=True, duration=2000)
        #     self.output *= Fade(is_in=False, duration=2000)
        # self.output *= self.filter1
        # self.output *= self.filter2
        
        if self.filter1 is not None:
            self.output *= self.filter1(self.filter1_freq)
        if self.filter2 is not None:
            self.output *= self.filter2(self.filter2_freq)

        # TODO: Fix sum of ADSR values being longer than the output file
        # if self.attack + self.decay + self.release <= duration:
        #     self.output = self.output * ADSR(attack=self.attack, decay=self.decay, sustain=self.sustain, release=self.release)
        # else:
        #     self.output = self.output * ADSR(attack=duration/3, decay=duration/3, sustain=self.sustain, release=duration/3)
        return self.output

if __name__ == '__main__':
    s = Synth({
        'lfo1_type': 'sine', 
        'lfo1_freq': 0.5, 
        'lfo1_depth': 0.5, 
        'lfo2_type': 'sine', 
        'lfo2_freq': 0.5, 
        'lfo2_depth': 0.5, 
        'osc1_freq': 200.0, 
        'osc1_relative_shift': 1.0, 
        'osc1_wave': 'square', 
        'osc1_detune': 30.0, 
        'osc2_freq': 400.0, 
        'osc2_relative_shift': 1.0, 
        'osc2_wave': 'triangle', 
        'osc2_detune': 30.0, 
        'n_voices': 6, 
        'sub_freq': 100.0, 
        'sub_wave': 'sine', 
        'sub_detune': 30.0, 
        'hf_noise_freq': 1000.0, 
        'hf_noise_type': 'sine', 
        'lf_noise_freq': 100.0, 
        'lf_noise_type': 'sine', 
        'filter1_type': 'lowpass', 
        'filter1_freq': 1000.0, 
        'filter2_type': 'na', 
        'filter2_freq': 0.0, 
        'filter3_type': 'na', 
        'filter3_freq': 0.0, 
        'reverb': 0.5, 
        'vibrato_freq': 0.5, 
        'vibrato_depth': 0.5, 
        'attack': 500.0, 
        'decay': 0.5, 
        'sustain': 0.5, 
        'release': 500.0, 
        'fade_in': 0.5, 
        'fade_out': 0.5})
    audio = s.generate_audio(69, 2e3)
    print(audio.realise(44100))