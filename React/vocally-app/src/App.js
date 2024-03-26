import axios from 'axios';
import React, { useState } from 'react'; 
function App() {
   const [audioFile, setAudioFile] = useState(null);
   const [analysisResult, setAnalysisResult] = useState(null);


   const handleAudioRecording = async () => {
       try {
           const mediaRecorder = new MediaRecorder({ audio: true });
           const chunks = [];


           mediaRecorder.addEventListener('dataavailable', (event) => {
               if (event.data.size > 0) {
                   chunks.push(event.data);
               }
           });


           mediaRecorder.addEventListener('stop', async () => {
               const blob = new Blob(chunks, { type: 'audio/wav' });
               setAudioFile(blob);


               const formData = new FormData();
               formData.append('audio', blob);


               const response = await axios.post('http://localhost:8000/process_audio', formData, {
                   headers: {
                       'Content-Type': 'multipart/form-data',
                   },
               });


               setAnalysisResult(response.data);
           });


           mediaRecorder.start();
           setTimeout(() => mediaRecorder.stop(), 3000); // Record for 3 seconds
       } catch (error) {
           console.error('Error recording audio:', error);
       }
   };


   return (
       <div className="App">
           <h1>Vocally</h1>
           <button onClick={handleAudioRecording}>Record Audio</button>
           {analysisResult && (
               <div>
                   <h2>Analysis Result</h2>
                   <p>Confidence Score: {analysisResult.confidence}</p>
                   <p>Clarity Score: {analysisResult.clarity}</p>
                   <p>Areas of Improvement: {analysisResult.improvement}</p>
               </div>
           )}
       </div>
   );
}


export default App;

/*
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
*/