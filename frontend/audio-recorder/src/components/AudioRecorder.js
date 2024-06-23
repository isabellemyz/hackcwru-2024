import React from 'react';
import axios from 'axios';
import { ReactMediaRecorder } from "react-media-recorder";

const AudioRecorder = ({ addMessage }) => {
  const handleStop = async (blobUrl, blob) => {
    const formData = new FormData();
    formData.append("file", blob, "audio.wav");

    // Send audio file to the server for transcription
    try {
      const transcribeResponse = await axios.post("http://localhost:8000/transcribe", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const transcription = transcribeResponse.data.transcription;
      addMessage({ type: 'user', text: transcription });  // Display the transcription in the UI
      getResponse(transcription);
    } catch (error) {
      console.error("Error transcribing audio:", error);
      addMessage({ type: 'bot', text: "Error transcribing audio." });
    }
  };

  // Send the transcribed text to get a response from another server endpoint
  const getResponse = async (transcription) => {
    try {
      const result = await axios.post("http://localhost:8000/get_response", {
        text: transcription
      });
      const aiResponse = result.data.response;  // Extract the response message
      addMessage({ type: 'bot', text: aiResponse });  // Display the AI response in the UI
    } catch (error) {
      console.error("Error getting response:", error);
      addMessage({ type: 'bot', text: "Error getting response." });
    }
  };

  return (
    <ReactMediaRecorder
      audio
      render={({ status, startRecording, stopRecording }) => (
        <>
          <p>{status}</p>
          <button onClick={startRecording} className="recording-button">Recording</button>
          <button onClick={stopRecording} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded m-2">Stop Recording</button>
        </>
      )}
      onStop={handleStop}
    />
  );
};

export default AudioRecorder;
