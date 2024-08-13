import React, { useState } from "react";
import ChatInterface from "./components/ChatInterface";
import AudioRecorder from "./components/AudioRecorder";
import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from "./components/Header";
import Status from "./components/Status";
import Camera from "./components/Camera";
import 'react-toastify/dist/ReactToastify.css';
import "./assets/toastStyles.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isCameraOn, setIsCameraOn] = useState(false);

// Function to add messages to the state
  const addMessage = (msg) => {
    setMessages(prevMessages => [...prevMessages, msg]);
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const toggleCamera = () => {
    setIsCameraOn(!isCameraOn);
  };

  return (
    <div className="App">
      <Header />
      <div className="layout-container">
        <div className="code-editor">
          <div className="box">
            <div className="box-title">Code Editor</div>
            <div className="box-content">code editor coming..</div>
          </div>
        </div>
        <div className="chat-section">
          <div className="box">
            <div className="box-title">Chat</div>
            <div className="box-content">
              <ChatInterface messages={messages} />
            </div>
          </div>
        </div>
        <div className="interactive-section">
          <div className="camera-section">
            <div className="box">
              <div className="box-title">Camera</div>
              <div className="box-content">
                <Camera isCameraOn={isCameraOn} />
              </div>
            </div>
          </div>
          <div className="bottom-section">
            <div className="microphone-section">
              <div className="box">
                <div className="box-title">Microphone</div>
                <div className="box-content">
                  <AudioRecorder addMessage={addMessage} clearMessages={clearMessages} />
                </div>
              </div>
            </div>
            <div className="status-section">
              <div className="box">
                <div className="box-title">Status</div>
                <div className="box-content">
                  <Status isCameraOn={isCameraOn} toggleCamera={toggleCamera} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default App;

