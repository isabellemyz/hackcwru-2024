import { useState, useReducer, useRef, useLayoutEffect } from 'react';
import axios from 'axios';
import * as toastConfig from "../utils/toastConfig";
import { refresh } from '../utils/AudioHelpers';


const AudioRecorder = ({ 
  clearMessages, 
  addMessage, 
  isRunning, 
  setIsRunning, 
  isListening, 
  setIsListening,
  dispatch,
}) => {
  const [offensiveWords, setOffensiveWords] = useState([]);
  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  useLayoutEffect(() => {
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

  const openWebSocketConnection = () => {
    const ws_url = 'ws://localhost:8000/listen';
    wsRef.current = new WebSocket(ws_url);

    const handleJsonMessage = (jsonData) => {
      const message = JSON.parse(jsonData);
      if (message.type === 'finish') {
        endConversation();
      } else {
        dispatch(message);
      }
    };
    

    wsRef.current.onmessage = (event) => {
      if (!(event.data instanceof ArrayBuffer)) {
        handleJsonMessage(event.data);
      }
    };

    wsRef.current.onclose = () => {
      endConversation();
    };
  };

  const closeWebSocketConnection = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }
  };

  const startMicrophone = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.addEventListener('dataavailable', e => {
      if (e.data.size > 0 && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(e.data);
      }
    });
    mediaRecorderRef.current.start(250);
  };

  const stopMicrophone = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.stream) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const startConversation = async () => {
    dispatch({ type: 'reset' });
    try {
      openWebSocketConnection();
      await startMicrophone();
      setIsRunning(true);
      setIsListening(true);
    } catch (err) {
      console.log('Error starting conversation:', err);
      endConversation();
    }
  };

  const endConversation = () => {
    closeWebSocketConnection();
    stopMicrophone();
    setIsRunning(false);
    setIsListening(false);
  };

  const toggleListening = () => {
    if (isListening) {
      mediaRecorderRef.current.pause();
    } else {
      mediaRecorderRef.current.resume();
    }
    setIsListening(!isListening);
  };

  return (
    <div className='audio-recorder-container'>
      <div className='controls'>
        <button
          className='start-end-button'
          onClick={isRunning ? endConversation : startConversation}
        >
          {isRunning ? 'End conversation' : 'Start conversation'}
        </button>
        <button
          className='mic-button'
          onClick={toggleListening}
          disabled={!isRunning}
        >
          {isListening ? 'Pause' : 'Resume'}
        </button>
      </div>
      <button
        onClick={() => refresh(clearMessages, addMessage)}
        className="refresh-button"
      >
        Refresh
      </button>
    </div>
  );
};

export default AudioRecorder;
