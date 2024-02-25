import streamlit as st
import numpy as np
import librosa
from tensorflow import keras
from keras.models import load_model
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import time

model = load_model('/Users/isabellez/vocally-project/backend/vocally_model.keras') 

# extract features from audio
def extract_features(audio_path):
    audio_data, sr = librosa.load(audio_path, sr=None)  # sr=None to retain original sampling rate

    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)

    #loudness
    rms = librosa.feature.rms(y=audio_data)

    # spectral contrast: measures the difference in amplitude between peaks and valleys in the spectrum
    # can be useful for distinguishing sounds with different timbral characteristics
    contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sr)

    # zero-crossing rate: the rate at which the signal changes its sign
    # can provide information about the level of abrupt changes or "noisiness" in the signal
    zcr = librosa.feature.zero_crossing_rate(y=audio_data)

    # aggregate statistics of features
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    rms_mean = np.mean(rms)
    rms_std = np.std(rms)
    contrast_mean = np.mean(contrast, axis=1)
    contrast_std = np.std(contrast, axis=1)
    zcr_mean = np.mean(zcr)
    zcr_std = np.std(zcr)

    labeled_features = {
        'mfccs_mean': np.sum(mfccs_mean),
        'mfccs_std': np.sum(mfccs_std),
        'rms_mean': rms_mean,
        'rms_std': rms_std,
        'contrast_mean': np.sum(contrast_mean),
        'contrast_std': np.sum(contrast_std),
        'zcr_mean': zcr_mean,
        'zcr_std': zcr_std
    }

    return labeled_features
    
# function to make predictions
def predict(audio_path):
    features = extract_features(audio_path)
    features_array = np.array([list(features.values())])
    prediction = model.predict(features_array)
    return prediction

# streamlit app
def main():
    st.set_page_config(page_title="Vocally")

    st.markdown("""
        <style>
            .centered {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="centered"><h1>VOCALLY</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">Improve your confidence and presentation skills today! Try out Vocally below :)</div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    
    if st.button("Record Audio"):
        duration = 3
        fs = 44100  # sampling freq
        recording = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype=np.int16)

        with st.spinner("Recording..."):
            sd.wait()
            st.success("Recording complete!") 

        # saving the recorded audio as an mp3 file
        audio_wav = AudioSegment(
            recording.tobytes(),
            frame_rate=fs,
            sample_width=recording.dtype.itemsize,
            channels=1
        )
        audio_wav.export("audio.mp3", format="mp3")

        prediction = predict("audio.mp3")
        conf_score = prediction[0][0]
        clar_score = prediction[0][1]

        #score should be between 0-10
        if conf_score > 10:
            conf_score = 10
        elif conf_score < 0:
            conf_score = 0
        if clar_score > 10:
            clar_score = 10
        elif clar_score < 0:
            clar_score = 0
        
        str_conf_score = str(round(conf_score, 1))
        conf_score_markdown = f'<div class="centered"><h3>CONFIDENCE SCORE:</h3><h3 style="color: #DE99D3;">{str_conf_score}</h3></div>'
        st.markdown(conf_score_markdown, unsafe_allow_html=True)

        str_clar_score = str(round(clar_score, 1))
        clar_score_markdown = f'<div class="centered"><h3>CLARITY SCORE:</h3><h3 style="color: #DE99D3;">{str_clar_score}</h3></div>'
        st.markdown(clar_score_markdown, unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()