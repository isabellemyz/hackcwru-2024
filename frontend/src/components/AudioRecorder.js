import React, { useState, useEffect }  from 'react';
import axios from 'axios';
import { ReactMediaRecorder } from "react-media-recorder";
import * as toastConfig from './toastConfig';

const AudioRecorder = ({ addMessage, clearMessages }) => {

  const [offensiveWords, setOffensiveWords] = useState([]);

  useEffect(() => {
    // Fetch offensive words from the configuration file
    const fetchOffensiveWords = async () => {
      try {
        const response = await axios.get('/offensiveWords.json');
        setOffensiveWords(response.data.offensiveWords);
      } catch (error) {
        console.error("Error fetching offensive words:", error);
      }
    };

    fetchOffensiveWords();
  }, []);

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

      // Empty Input Validation
      if (!transcription.trim()) {
        toastConfig.showToast("Input cannot be empty!", 'error');
        return;
      }

      // Offensive Words Validation
      const containsOffensiveWords = offensiveWords.some(word => transcription.toLowerCase().includes(word));
      if (containsOffensiveWords) {
        toastConfig.showToast("Inappropriate language and cannot be processed.", 'error');
        return;
      }

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

      const jsonObject = JSON.parse(result.data.response);
      const key = Object.keys(jsonObject)[0];
      const aiResponse = jsonObject[key];

      addMessage({ type: 'bot', text: aiResponse });  // Display the AI response in the UI
    } catch (error) {
      console.error("Error getting response:", error);
      addMessage({ type: 'bot', text: "Error getting response." });
    }
  };

  const refresh = async () => {
    try {
      await axios.delete("http://localhost:8000/clear_response");
      clearMessages();
      addMessage({ type: 'bot', text: "Conversation history has been cleared."});
    } catch (error) {
      console.error("Error clearing response:", error);
      addMessage({ type: 'bot', text: "Error clearing response." });
    }
  }

  return (
    <ReactMediaRecorder
      audio
      render={({ status, startRecording, stopRecording }) => (
        <>
          <p>{status}</p>
          <button onClick={startRecording} className="recording-button">Recording</button>
          <button onClick={stopRecording} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded m-2">Stop Recording</button>
          <button onClick={refresh} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2">Refresh</button>
        </>
      )}
      onStop={handleStop}
    />
  );
};

export default AudioRecorder;
