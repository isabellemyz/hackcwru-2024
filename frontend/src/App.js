import React, { useState, useReducer } from "react";
import ChatInterface from "./components/ChatInterface";
import AudioRecorder from "./components/AudioRecorder";
import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from "./components/Header";
import Status from "./components/Status";
import Camera from "./components/Camera";
import conversationReducer from './components/ConversationReducer';
import 'react-toastify/dist/ReactToastify.css';
import "./assets/toastStyles.css";

const initialConversation = { messages: [], finalTranscripts: [], interimTranscript: '' };

const App = () => {
  const [messages, setMessages] = useState([]);
  const [conversation, dispatch] = useReducer(conversationReducer, initialConversation);
  const [isRunning, setIsRunning] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const currentTranscript = [...conversation.finalTranscripts, conversation.interimTranscript].join(' ');

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
            <ChatInterface
              conversation={conversation}
              currentTranscript = {currentTranscript}
            />
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
                <AudioRecorder 
                  clearMessages={clearMessages}
                  isRunning={isRunning}
                  setIsRunning={setIsRunning}
                  isListening={isListening}
                  setIsListening={setIsListening}
                  dispatch={dispatch}  
                />
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
}

export default App;
