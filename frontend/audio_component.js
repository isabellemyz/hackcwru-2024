// UNTESTED AND UNEDITED CHATGPT CODE

// src/components/AudioRecorder.js
// import React, { useState, useEffect, useRef } from 'react';
// import { useEffectOnce } from 'react-use';

// const AudioRecorder = () => {
//     const [isRecording, setIsRecording] = useState(false);
//     const [audioChunks, setAudioChunks] = useState([]);
//     const mediaRecorderRef = useRef(null);
//     const audioContextRef = useRef(null);
//     const mediaStreamRef = useRef(null);
//     const analyserRef = useRef(null);
//     const dataArrayRef = useRef(null);
//     const scriptProcessorRef = useRef(null);

//     useEffectOnce(() => {
//         const init = async () => {
//             const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//             mediaStreamRef.current = stream;
//             audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
//             analyserRef.current = audioContextRef.current.createAnalyser();
//             scriptProcessorRef.current = audioContextRef.current.createScriptProcessor(2048, 1, 1);
//             const source = audioContextRef.current.createMediaStreamSource(stream);

//             source.connect(analyserRef.current);
//             analyserRef.current.connect(scriptProcessorRef.current);
//             scriptProcessorRef.current.connect(audioContextRef.current.destination);

//             analyserRef.current.fftSize = 2048;
//             const bufferLength = analyserRef.current.frequencyBinCount;
//             dataArrayRef.current = new Uint8Array(bufferLength);

//             scriptProcessorRef.current.onaudioprocess = () => {
//                 analyserRef.current.getByteTimeDomainData(dataArrayRef.current);
//                 const maxVolume = Math.max(...dataArrayRef.current);
//                 if (maxVolume > 128) {
//                     if (!isRecording) {
//                         startRecording();
//                     }
//                 } else {
//                     if (isRecording) {
//                         stopRecording();
//                     }
//                 }
//             };
//         };

//         init();

//         return () => {
//             mediaStreamRef.current.getTracks().forEach(track => track.stop());
//             scriptProcessorRef.current.disconnect();
//             analyserRef.current.disconnect();
//             audioContextRef.current.close();
//         };
//     });

//     const startRecording = () => {
//         setIsRecording(true);
//         mediaRecorderRef.current = new MediaRecorder(mediaStreamRef.current);
//         mediaRecorderRef.current.ondataavailable = (event) => {
//             if (event.data.size > 0) {
//                 setAudioChunks(prev => [...prev, event.data]);
//             }
//         };
//         mediaRecorderRef.current.start();
//     };

//     const stopRecording = () => {
//         setIsRecording(false);
//         mediaRecorderRef.current.stop();
//     };

//     const handleSendAudio = async () => {
//         const blob = new Blob(audioChunks, { type: 'audio/webm' });
//         const formData = new FormData();
//         formData.append('file', blob, 'recording.webm');

//         await fetch('http://localhost:8000/upload', {
//             method: 'POST',
//             body: formData,
//         });

//         setAudioChunks([]);
//     };

//     return (
//         <div>
//             <button onClick={handleSendAudio} disabled={!audioChunks.length}>Send Audio</button>
//         </div>
//     );
// };

// export default AudioRecorder;
