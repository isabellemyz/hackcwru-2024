import React from 'react';
import VideocamIcon from '@mui/icons-material/Videocam';
import VideocamOffIcon from '@mui/icons-material/VideocamOff';
import { red } from '@mui/material/colors';

const Status = ({ isCameraOn, toggleCamera }) => {
  return (
    <div className="status-container">
      <div className="status-item" onClick={toggleCamera}>
        {isCameraOn ? (
          <VideocamIcon className="camera-icon on" color="success" sx={{ transition: 'all 0.3s ease-in-out' }} />
        ) : (
          <VideocamOffIcon className="camera-icon off" sx={{ color: red[500], transition: 'all 0.3s ease-in-out' }} />
        )}
      </div>

      
    </div>
  );
};

export default Status;
