import React from 'react';

const ChatInterface = ({ messages }) => {
  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <span className="sender">{msg.type === 'user' ? 'YOU' : 'INTERVIEWER'}</span>
            <span className="message-text">{msg.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatInterface;
