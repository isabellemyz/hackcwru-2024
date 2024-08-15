import React, { useRef, useEffect } from 'react';
import * as toastConfig from '../utils/toastConfig';

const Camera = ({ isCameraOn }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (isCameraOn) {
      startCamera();
    } else {
      stopCamera();
    }
  }, [isCameraOn]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      toastConfig.showToast('Error accessing camera', 'error');
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  return (
    <div className="camera-container">
      {isCameraOn && (
        <div className="video-container">
          <video ref={videoRef} autoPlay playsInline muted style={{ transform: 'scaleX(-1)' }} />
        </div>
      )}
    </div>
  );
};

export default Camera;
