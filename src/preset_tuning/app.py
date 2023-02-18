import streamlit as st
# st.write(st.__version__)
import pandas as pd
import numpy as np
import time
import os
from io import BytesIO
import json
import ambientmusicsynthesis.synth as s
# from dataclasses import dataclass, asdict, is_dataclass

# def dataclass_from_dict(cls, d):
#     return cls(**d)
# @dataclass
# class SegmentParams:
#     lfo1_type: str
#     lfo1_freq: float
#     lfo1_depth: float
#     lfo2_type: str
#     lfo2_freq: float
#     lfo2_depth: float
#     osc1_freq: float
#     osc1_relative_shift: float
#     osc1_wave: str
#     osc1_detune: float
#     osc2_freq: float
#     osc2_relative_shift: float
#     osc2_wave: str
#     osc2_detune: float
#     n_voices: int
#     sub_freq: float
#     sub_wave: str
#     sub_detune: float
#     hf_noise_freq: float
#     hf_noise_type: str
#     lf_noise_freq: float
#     lf_noise_type: str
#     filter1_type: str
#     filter1_freq: float
#     filter2_type: str
#     filter2_freq: float
#     filter3_type: str
#     filter3_freq: float
#     reverb: float
#     vibrato_freq: float
#     vibrato_depth: float
#     attack: float
#     decay: float
#     sustain: float
#     release: float
#     fade_in: float
#     fade_out: float

# @dataclass
# class Params:
#     "1": SegmentParams
#     "2": SegmentParams
#     "3": SegmentParams
#     "4": SegmentParams
#     "5": SegmentParams

def play_audio(params):
    synth=s.Synth(params)
    audio = synth.generate_audio(42,5e3)
    print(audio)
    b=BytesIO(audio.realise(44100))
    # b = BytesIO(synth.generate_audio(42,5e3))
    st.audio(b, format='audio/wav')

def save_preset(params, segment_number):
    output_params = json.load(open(os.path.join(os.path.dirname(__file__),'tmp.json')))
    output_params[segment_number] = params
    st.json(output_params)
    with open(os.path.join(os.path.dirname(__file__),'tmp.json'), 'w') as f:
        print("Saving file")
        json.dump(output_params, f)
    

def main():
    st.title("Tune the parameters for the synthesis of each emotional segment (1-5)")
    with st.form("parameters"):
        segment_choice = st.selectbox("Pick a segment to design sound for", ["1","2","3","4","5"])
        st.text("LFO params")
        lfo1_type = st.selectbox("lfo1_type",['sine','square','sawtooth','triangle'])
        lfo1_freq = st.slider("lfo1_freq", min_value=0.0, max_value=16.0, step=0.1)
        lfo1_depth = st.slider("lfo1_depth", min_value=0.0, max_value=0.5, step=0.1)
        st.text("")
        lfo2_type = st.selectbox("lfo2_type",['sine','square','sawtooth','triangle'])
        lfo2_freq = st.slider("lfo2_freq", min_value=0.0, max_value=16.0, step=0.1)
        lfo2_depth = st.slider("lfo2_depth", min_value=0.0, max_value=0.5, step=0.1)
        st.text("")
        st.text("")
        st.text("Oscillator params")
        osc1_freq = st.slider("osc1_freq", min_value=0.0, max_value=16.0, step=0.1)
        osc1_relative_shift = st.slider("osc1_relative_shift", min_value=0.0, max_value=16.0, step=0.1)
        osc1_wave = st.selectbox("osc1_wave",['sine','square','sawtooth','triangle'])
        osc1_detune = st.slider("osc1_detune", min_value=0.0, max_value=16.0, step=0.1)
        st.text("")
        osc2_freq = st.slider("osc2_freq", min_value=0.0, max_value=16.0, step=0.1)
        osc2_relative_shift = st.slider("osc2_relative_shift", min_value=0.0, max_value=16.0, step=0.1)
        osc2_wave = st.selectbox("osc2_wave",['sine','square','sawtooth','triangle'])
        osc2_detune = st.slider("osc2_detune", min_value=0.0, max_value=16.0, step=0.1)
        st.text("")
        st.text("")
        st.text("Number of voices")
        n_voices = st.slider("n_voices", min_value=0, max_value=16, step=1)
        st.text("")
        st.text("")
        st.text("Sub oscillator params")
        sub_freq = st.slider("sub_freq", min_value=0.0, max_value=16.0, step=0.1)
        sub_wave = st.selectbox("sub_wave",['sine','square','sawtooth','triangle'])
        sub_detune = st.slider("sub_detune", min_value=0.0, max_value=16.0, step=0.1)
        st.text("")
        st.text("")
        st.text("Noise params")
        hf_noise_freq = st.slider("hf_noise_freq", min_value=0.0, max_value=16.0, step=0.1)
        hf_noise_type = st.selectbox("hf_noise_type",['sine','square','sawtooth','triangle'])
        st.text("") 
        lf_noise_freq = st.slider("lf_noise_freq", min_value=0.0, max_value=16.0, step=0.1)
        lf_noise_type = st.selectbox("lf_noise_type",['sine','square','sawtooth','triangle'])
        st.text("")
        st.text("")
        st.text("Filter params")
        filter1_type = st.selectbox("filter1_type",['na','lowpass', 'highpass', 'bandpass', 'bandstop', 'lowshelf', 'highshelf'])
        filter1_freq = st.slider("filter1_freq", min_value=20.0, max_value=20000.0, step=1.0)
        st.text("")
        filter2_type = st.selectbox("filter2_type",['na','lowpass', 'highpass', 'bandpass', 'bandstop', 'lowshelf', 'highshelf'])
        filter2_freq = st.slider("filter2_freq", min_value=20.0, max_value=20000.0, step=1.0)
        st.text("")
        filter3_type = st.selectbox("filter3_type",['na','lowpass', 'highpass', 'bandpass', 'bandstop', 'lowshelf', 'highshelf'])
        filter3_freq = st.slider("filter3_freq", min_value=20.0, max_value=20000.0, step=1.0)
        st.text("")
        
        reverb = st.slider("reverb", min_value=0.0, max_value=16.0, step=0.1)
        vibrato_freq = st.slider("vibrato_freq", min_value=0.0, max_value=16.0, step=0.1)
        vibrato_depth = st.slider("vibrato_depth", min_value=0.0, max_value=16.0, step=0.1)
        
        attack = st.slider("attack", min_value=0.0, max_value=16.0, step=0.1)
        decay = st.slider("decay", min_value=0.0, max_value=16.0, step=0.1)
        sustain = st.slider("sustain", min_value=0.0, max_value=16.0, step=0.1)
        release = st.slider("release", min_value=0.0, max_value=16.0, step=0.1)
        
        fade_in = st.slider("fade_in", min_value=0.0, max_value=16.0, step=0.1)
        fade_out = st.slider("fade_out", min_value=0.0, max_value=16.0, step=0.1)

        submitted = st.form_submit_button("Test params")
        if submitted:
            params = {"lfo1_type":lfo1_type,"lfo1_freq":lfo1_freq,"lfo1_depth":lfo1_depth,"lfo2_type":lfo2_type,"lfo2_freq":lfo2_freq,"lfo2_depth":lfo2_depth,"osc1_freq":osc1_freq,"osc1_relative_shift":osc1_relative_shift,"osc1_wave":osc1_wave,"osc1_detune":osc1_detune,"osc2_freq":osc2_freq,"osc2_relative_shift":osc2_relative_shift,"osc2_wave":osc2_wave,"osc2_detune":osc2_detune,"n_voices":n_voices,"sub_freq":sub_freq,"sub_wave":sub_wave,"sub_detune":sub_detune,"hf_noise_freq":hf_noise_freq,"hf_noise_type":hf_noise_type,"lf_noise_freq":lf_noise_freq,"lf_noise_type":lf_noise_type,"filter1_type":filter1_type,"filter1_freq":filter1_freq,"filter2_type":filter2_type,"filter2_freq":filter2_freq,"filter3_type":filter3_type,"filter3_freq":filter3_freq, "reverb":reverb,"vibrato_freq":vibrato_freq,"vibrato_depth":vibrato_depth,"attack":attack,"decay":decay,"sustain":sustain,"release":release,"fade_in":fade_in,"fade_out":fade_out}
            with open(os.path.join(os.path.dirname(__file__),f'{segment_choice}_tmp.json'), 'w') as f:
                json.dump(params,f)
            params = json.load(open(os.path.join(os.path.dirname(__file__),f'{segment_choice}_tmp.json'), 'r'))
            st.json(params)
            play_audio(params)
    
    save_button = st.button("Save (Hit after every segment, before switching to a new segment)")
    if save_button:
        save_params(segment_choice)

def save_params(segment_number):
    params = json.load(open(os.path.join(os.path.dirname(__file__),f'{segment_number}_tmp.json'), 'r'))
    output_params = json.load(open(os.path.join(os.path.dirname(__file__),f'tmp.json'), 'r'))
    output_params[segment_number] = params
    with open(os.path.join(os.path.dirname(__file__),f'tmp.json'), 'w') as f:
        json.dump(output_params,f)
    st.json(output_params)


if __name__ == '__main__':
    main()






















# def get_params_for_segment_no_overwrite(segment_number,output_params):
#     col1, col2, col3 = st.columns(3)
#     st.json(output_params)
#     d=output_params[segment_number]
#     st.json(d)
#     with st.form("parameters"):
#         with col1:
#             st.header("LFO Parameters")
#             lfo1_type = st.selectbox("lfo1_type",['sine','square','sawtooth','triangle'])
#             lfo1_freq = st.slider("lfo1_freq", min_value=0.0, max_value=16.0, step=0.1)
#             lfo1_depth = st.slider("lfo1_depth", min_value=0.0, max_value=0.5,step=0.1)
#             st.text("")
#             st.text("")
#             lfo2_type = st.selectbox("lfo2_type",['sine','square','sawtooth','triangle'])
#             lfo2_freq = st.slider("lfo2_freq", min_value=0.0, max_value=16.0, step=0.1)
#             lfo2_depth = st.slider("lfo2_depth", min_value=0.0, max_value=0.5, step=0.1)
#             st.text("")
#         saved=st.form_submit_button("Save")
#         if saved:
#             d['lfo1_type']=lfo1_type
#             d['lfo1_freq']=lfo1_freq
#             d['lfo1_depth']=lfo1_depth
#             d['lfo2_type']=lfo2_type
#             d['lfo2_freq']=lfo2_freq
#             d['lfo2_depth']=lfo2_depth
#             st.json(d)
#             print('SAVING PRESET')
#             print(output_params)
#             save_preset(d, segment_number)
#             return d#{'lfo1_type':lfo1_type,'lfo1_freq':lfo1_freq,'lfo1_depth':lfo1_depth,'lfo2_type':lfo2_type,'lfo2_freq':lfo2_freq,'lfo2_depth':lfo2_depth}

# def save_preset(params, segment_number):
#     output_params = json.load(open(os.path.join(os.path.dirname(__file__),'tmp.json')))
#     output_params[segment_number] = params
#     st.json(output_params)
#     with open(os.path.join(os.path.dirname(__file__),'tmp.json'), 'w') as f:
#         print("Saving file")
#         json.dump(output_params, f)




# def main():
#     st.title('Tune the parameters for the synthesis of each emotional segment (1-5)')
#     segment_choice = st.sidebar.selectbox("Pick a segment to design sound for", ["1","2","3","4","5"])
#     save_preset = st.sidebar.button("Save Preset")
#     # output_params={1:{},2:{},3:{},4:{},5:{}}
#     keys = ['lfo1_type','lfo1_freq','lfo1_depth','lfo2_type','lfo2_freq','lfo2_depth','osc1_freq','osc1_relative_shift','osc1_wave','osc1_detune','osc2_freq','osc2_relative_shift','osc2_wave','osc2_detune','n_voices','sub_freq','sub_wave','sub_detune','hf_noise_freq','hf_noise_type','lf_noise_freq','lf_noise_type','filter1_type','filter1_freq','filter2_type','filter2_freq','filter3_type','filter3_freq','reverb','vibrato_freq','vibrato_depth','attack','decay','sustain','release','fade_in','fade_out']
#     # print(len(output_params[segment_choice]))
#     output_params = json.load(open(os.path.join(os.path.dirname(__file__),'tmp.json')))
#     if len(output_params[segment_choice]) == 0:
#         print('Getting new parameter set')
#         params = get_params_for_segment_no_overwrite(segment_choice, output_params)
#     else:
#         st.write("Do you want to overwrite an existing parameter")
    
    
#     test_audio = st.button('Play audio')
#     if test_audio:
#         play_audio(params)
    
#     if save_preset:
#         output_params = json.load(open(os.path.join(os.path.dirname(__file__),'tmp.json')))
#         output_params[segment_choice] = params
#         st.json(output_params)
#         with open(os.path.join(os.path.dirname(__file__),'tmp.json'), 'w') as f:
#             print("Saving file")
#             json.dump(output_params, f)

# # def main():
# #     with st.form("my_form"):
# #         st.write("Inside the form")
# #         slider_val = st.slider("Form slider")
# #         checkbox_val = st.checkbox("Form checkbox")

# #         # Every form must have a submit button.
# #         submitted = st.form_submit_button("Submit")
# #         if submitted:
# #             st.write("slider", slider_val, "checkbox", checkbox_val)

# #     st.write("Outside the form")

# if __name__=='__main__':
#     main()

