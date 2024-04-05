from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from typing import List
import librosa
import numpy as np
import joblib
from sklearn_porter import Porter


app = FastAPI()


# Define input model for audio data
class AudioInput(BaseModel):
   audio: bytes


# Load the pretrained model
model = joblib.load('/Users/tanujkannan/Vocally/vocally_model_decisionTree.joblib')


# Function to extract features from audio
def extract_features(audio_path):
   # Load the audio file using librosa
   audio_data, sr = librosa.load(audio_path, sr=None)  # sr=None to retain original sampling rate


   # Extract MFCCs (Mel-frequency cepstral coefficients) from the audio
   mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
  
   # Calculate the mean and standard deviation of MFCCs
   mfccs_mean = np.mean(mfccs, axis=1)
   mfccs_std = np.std(mfccs, axis=1)


   # Calculate the root mean square (RMS) energy of the audio
   rms = librosa.feature.rms(y=audio_data)
   rms_mean = np.mean(rms)
   rms_std = np.std(rms)


   # Calculate spectral contrast features
   contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sr)
   contrast_mean = np.mean(contrast, axis=1)
   contrast_std = np.std(contrast, axis=1)


   # Calculate zero-crossing rate (ZCR)
   zcr = librosa.feature.zero_crossing_rate(y=audio_data)
   zcr_mean = np.mean(zcr)
   zcr_std = np.std(zcr)


   # Aggregate the extracted features into a dictionary
   extracted_features = {
       'mfccs_mean': np.sum(mfccs_mean),
       'mfccs_std': np.sum(mfccs_std),
       'rms_mean': rms_mean,
       'rms_std': rms_std,
       'contrast_mean': np.sum(contrast_mean),
       'contrast_std': np.sum(contrast_std),
       'zcr_mean': zcr_mean,
       'zcr_std': zcr_std
   }


   return extracted_features


# API endpoint to process uploaded audio
@app.post("/process_audio")
async def process_audio(audio_data: AudioInput):
   # Save the uploaded audio file
   with open("uploaded_audio.wav", "wb") as audio_file:
       audio_file.write(audio_data.audio)


   # Extract features from the uploaded audio
   extracted_features = extract_features("uploaded_audio.wav")


   # Make predictions using the model
   prediction = model.predict(np.array([list(extracted_features.values())]))


   # Process the prediction result as needed
   confidence_score = prediction[0][0]
   clarity_score = prediction[0][1]
   improvement = ""


   # Return the analysis result
   return {
       "confidence": confidence_score,
       "clarity": clarity_score,
       "improvement": improvement
   }