import os
from icecream import ic
ic.configureOutput(prefix='Debug | ')#, includeContext=True)
# ic.disable()
import gensound
from gensound.signals import Sine, Sawtooth, Square, Triangle, WhiteNoise, Silence, PinkNoise, Mix, WAV
from gensound.effects import OneImpulseReverb, Vibrato
from gensound.filters import SimpleBandPass, SimpleHPF, SimpleLPF, SimpleHighShelf, SimpleLowShelf
from gensound.transforms import ADSR, Fade, Amplitude, CrossFade
from gensound.curve import SineCurve

import json
class Synth():
    def __init__(self, params):
        # self.preset = preset
        # if self.preset == 'default':
            # load json file containing default settings
            # data = json.load(open('../presets/default.json'))
        # data = json.load(open(os.path.join(path_to_preset,'timbre.json')))[self.preset]
        self.__dict__ = params
        # self.mood_map = mood_map

    def _setparam(self, param, value):
        setattr(self, param, value)
    def shift_freq_by_cents(self, freq, cents):
        return freq*(10**(cents/(1200*3.322038403)))
    def semitones_to_cents(self, semitones):
        return semitones*100
    def cents_to_semitones(self, cents):
        return cents/100
    def detuned_voices(self, pitch, duration, detune_range, n_voices, wave_type='square'):
        # n_voices = how many oscillators in the array
        # detune_range = the difference in cents between the highest and lowest oscillators in the array
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
        if isinstance(pitch, str):
            # print([f"{pitch}{round(cents):+}" for cents in all_cents])
            return gensound.mix([f(f"{pitch}{round(cents):+}", duration) for cents in all_cents])
        elif (isinstance(pitch, int)) or isinstance(pitch, int):
            return gensound.mix([f(self.shift_freq_by_cents(pitch,cents),duration) for cents in all_cents])
    def generate_audio(self, pitch,duration):
        # self._update()
        self.pitch = pitch
        # 2 LFOS for amplitude modulation

        self.lfo1 = Amplitude(SineCurve(frequency=self.lfo1_freq, depth=self.lfo1_depth, baseline=0.5, duration=duration))
        self.lfo2 = Amplitude(SineCurve(frequency=self.lfo2_freq, depth=self.lfo2_depth, baseline=0.5, duration=duration))

        # 2 oscillators for the main sound
        self.osc1 = self.detuned_voices(self.pitch, duration=duration,detune_range = self.osc1_detune, n_voices = self.n_voices, wave_type=self.osc1_wave)
        self.osc2 = self.detuned_voices(self.pitch, duration=duration,detune_range = self.osc2_detune, n_voices = self.n_voices, wave_type=self.osc2_wave)
        # 1 oscillator for the sub bass
        self.sub_bass = self.detuned_voices(self.sub_freq, duration=duration,detune_range = self.sub_detune, n_voices = self.n_voices, wave_type='sine')
        # 1 oscillator for the high frequency noise
        self.high_freq_noise = WhiteNoise(duration=duration)
        # 1 oscillator for the low frequency noise
        self.low_freq_noise = PinkNoise(duration=duration)
        # Filters

        # EFFECTS
        #   - Reverb
        #   - Vibrato

        # AMPLITUDE ENVELOPES
        #   - 2 ADSR envelopes
        #   - Fade in and out

        # apply lfo1 and lfo2 to osc1 and osc2 amplitude
        if self.lfo1_freq != 0:
            # self.lfo1 = self.lfo1 * ADSR(attack=self.attack, decay=self.decay, sustain=self.sustain, release=self.release)
            self.lfo1 = self.osc1 * self.lfo1
        if self.lfo2_freq != 0:
            # self.lfo2 = self.lfo2 * ADSR(attack=self.attack, decay=self.decay, sustain=self.sustain, release=self.release)
            self.lfo2 = self.osc2 * self.lfo2

        self.output = gensound.mix([self.osc1, self.osc2, self.sub_bass, self.high_freq_noise, self.low_freq_noise])
        if duration < 0.5:
            self.output = self.output * Fade(is_in=True,duration=duration/3)
            self.output = self.output * Fade(is_in=False,duration=duration/3)
        else:
            self.output *= Fade(is_in=True, duration=2000)
            self.output *= Fade(is_in=False, duration=2000)
        self.output = self.output * ADSR(attack=self.attack, decay=self.decay, sustain=self.sustain, release=self.release)
        
        return self.output


if __name__ == '__main__':
    synth = Synth(params={
        "lfo1_type" : "sine",
        "lfo1_freq": 0.5,
        "lfo1_depth" : 0.5,
        "lfo2_type" : "sine",
        "lfo2_freq" : 0.5,
        "lfo2_depth" : 0.5,
        "osc1_freq" : 400,
        "osc1_wave" : "square",
        "osc1_detune": 30,
        "osc2_freq" : 400,
        "osc2_wave" : "triangle",
        "osc2_detune": 30,
        "n_voices" : 6,
        "sub_freq" : 100,
        "sub_wave" : "sine",
        "sub_detune" : 30,
        "hf_noise_freq" : 1000,
        "hf_noise_wave" : "sine",
        "lf_noise_freq" : 100,
        "lf_noise_wave" : "sine",
        "filter1_type" : "lowpass",
        "filter1_freq" : 1000,
        "filter2_type" : "na", 
        "filter2_freq" : 0,
        "filter3_type" : "na",
        "filter3_freq" : 0,
        "reverb" : 0.5,
        "vibrato_freq" : 0.5,
        "vibrato_depth" : 0.5,
        "attack" : 5e2,
        "decay" : 0.5,
        "sustain" : 0.5,
        "release" : 5e2,
        "fade_in" : 0.5,
        "fade_out" : 0.5,
        "automation" : {
            "filter1_freq_type" : "constant",
            "filter1_freq_rate" : 0,
            "filter2_freq_type" : "constant",
            "filter2_freq_rate" : 0,
            "filter3_freq_type" : "constant",
            "filter3_freq_rate" : 0
            }
        })
    synth.generate_audio(440, 4*1e3).play()