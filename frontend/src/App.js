import React, { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import AudioRecorder from "./components/AudioRecorder";
import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "./assets/toastStyles.css";

const App = () => {
  const [messages, setMessages] = useState([]);

  // Function to add messages to the state
  const addMessage = (msg) => {
    setMessages(prevMessages => [...prevMessages, msg]);
  };

  // Function to clear all messages
  const clearMessages = () => {
    setMessages([]);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-2xl font-bold">Vocally </h1>
        <ChatInterface messages={messages} />
        <AudioRecorder addMessage={addMessage} clearMessages={clearMessages}/>
        <ToastContainer />
      </header>
    </div>
  );
};

export default App;
