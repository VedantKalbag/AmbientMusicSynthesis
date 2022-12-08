import os
import numpy as np
import json
import pytest
from ambientmusicsynthesis.ambientmusicsynthesis import AmbientMusicSynthesis
# ams = AmbientMusicSynthesis()
# audio = ams.generate_audio(90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, sample_rate=44100)
   
# TESTING AMBIENTMUSICSYNTHESIS CLASS
def test_export_audio():
    ams = AmbientMusicSynthesis()
    audio = ams.generate_audio(90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, sample_rate=44100)
    ams.export_audio('test_2.wav')
    audio.export('test_3.wav')
    assert os.path.exists('test_2.wav')
    assert os.path.exists('test_3.wav')
    #TODO: add assert to check that the files are the same after loading
    #TODO: add assert to check that both files are of the same length, equal to the desired length

    os.remove('test_2.wav')
    os.remove('test_3.wav')

@pytest.mark.parametrize("duration, mood_map, sample_rate", [
    (90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, 44100),
    (90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, 48000),
    (90, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, 96000),
    (45, {0.0:1, 20.3:2, 45:3}, 44100),
    (45, {0.0:1, 20.3:2, 45:3}, 48000),
    (45, {0.0:1, 20.3:2, 45:3}, 96000),
])
def test_generate_audio(duration, mood_map, sample_rate):
    ams = AmbientMusicSynthesis()
    audio = ams.generate_audio(duration, mood_map, sample_rate)
    assert audio != None

#@pytest.mark.skip(reason="duration parameter to be removed and inferred from the mood_map")
@pytest.mark.parametrize("duration",[
    (45),
    (-1),
    ("0"),
    ("90")
])
def test_generate_audio_with_invalid_duration(duration):
    ams = AmbientMusicSynthesis()
    with pytest.raises(AssertionError):
        ams.generate_audio(duration, {0.0:1, 20.3:2, 40.6:3, 60.9:4, 81.2:5, 90:1}, 44100)

# TODO: write test to ensure that the keys in the dict are all in ascending order

@pytest.mark.parametrize("duration, mood_map", [
    (45, {0.0:1, 20.3:2, 47:3}),
    (45, {0.0:1, 20.3:2, 44:3}),
    (45, {0.0:1, 20.3:2, -1:3}),
])
@pytest.mark.xfail
def test_generate_audio_with_invalid_mood_map(duration, mood_map):
    ams = AmbientMusicSynthesis()
    with pytest.raises(AssertionError):
        ams.generate_audio(duration, mood_map, 44100)

# TESTING SYNTHESIS CLASS
@pytest.fixture(scope="session")
def synth():
    from ambientmusicsynthesis.synth import Synth
    d = json.load(open('presets/timbre.json'))
    return Synth(d['default'])


def test_synthesis_with_invalid_preset():
    from ambientmusicsynthesis.synth import Synth
    with pytest.raises(TypeError):
        synthesis = Synth()

@pytest.mark.parametrize("midi_number, expected_freq", [
    (127, 12543.85),
    (0, 8.18),
    (21, 27.50),
    (69, 440)
])
def test_midi_to_freq(midi_number, expected_freq, synth):
    assert np.round(synth.midi_to_freq(midi_number),2) == np.round(expected_freq,2)

@pytest.mark.parametrize("freq, cents, expected_freq", [
    (100, 100, 100*1.059463),
    (1000, 100, 1000*1.059463),
    (100, 200, 100*1.122462),
    (1000, 200, 1000*1.122462),
    (100, 10, 100*1.005793),
    (1000, 10, 1000*1.005793)
])
def test_shift_freq_by_cents(freq, cents, expected_freq, synth):
    assert np.round(synth.shift_freq_by_cents(freq, cents),2) == np.round(expected_freq,2)

def test_semitones_to_cents(synth):
    assert synth.semitones_to_cents(1) == 100

def test_octave_to_multiplier(synth):
    assert synth.octave_to_multiplier(1) == 2
    assert synth.octave_to_multiplier(2) == 4
    assert synth.octave_to_multiplier(3) == 8

# TESTING MUSICAL PARAMETERS CLASS
@pytest.fixture(scope="session")
def musical_parameters():
    from ambientmusicsynthesis.musical_params_unified import MusicalParameters
    d = json.load(open('presets/musical_params.json'))
    return MusicalParameters(duration=90, 
                        ending_chord_min_length=2, 
                        starting_key='C', 
                        starting_length="VL", 
                        starting_note_density=3, 
                        starting_octave=4, 
                        preset_dict=d)


@pytest.mark.parametrize("note, octave, expected_midi_number", [
    ('C', 3, 48),
    ('C#', 4, 61),
    ('D', 5, 74),
    ('A', 4, 69),
    ('A#', 4, 70)
])
def test_note_to_number(note, octave, expected_midi_number, musical_parameters):
    assert musical_parameters.note_to_number(note, octave) == expected_midi_number

@pytest.mark.parametrize("midi_number, expected_note_number, expected_note, expected_octave", [
    (48, 0, 'C', 3),
    (61, 1, 'C#', 4),
    (74, 2, 'D', 5),
    (69, 9, 'A', 4),
    (70, 10, 'A#', 4)
])
def test_number_to_note(midi_number, expected_note_number, expected_note, expected_octave, musical_parameters):
    assert musical_parameters.number_to_note(midi_number) == (expected_note_number, expected_note, expected_octave)

def test_list_flatten(musical_parameters):
    assert musical_parameters.flatten([1,2,3,4,5]) == [1,2,3,4,5]
    assert musical_parameters.flatten([1,[2,3],[4,5]]) == [1,2,3,4,5]
    assert musical_parameters.flatten([1,[2,3],[4,[5]]]) == [1,2,3,4,5]
    assert musical_parameters.flatten([1,[2,3],[4,[5,[6]]]]) == [1,2,3,4,5,6]

@pytest.mark.skip(reason="To implement") # TODO: Implement this test
@pytest.mark.parametrize("chord", [
    ([60, 64, 67]),
    ([60, 64, 67, 70])
])
def test_get_nearest_chord(chord, expected_chords, musical_parameters):
    selected_chord,chords = musical_parameters.get_nearest_chord(chord)
    # TODO: CHECK THT EVERY CHORD IN CHORDS IS DIFFERENT IN ONLY 1 SPOT, AND THE OTHER LEN-1 SPOTS ARE THE SAME
    print(chords)
    # assert chords == expected_chords
    assert selected_chord in expected_chords
