import React from 'react';

const ChatInterface = ({ conversation, currentTranscript }) => {
  return (
    <div className="chat-container">
      <div className="chat-box">
      {conversation.messages.map(({ role, content }, idx) => (
        <div key={idx}>
          <span className="sender">{role === 'user' ? 'YOU' : 'INTERVIEWER'}</span>
          <span className="message-text">{content}</span>
        </div>
      ))}
        {currentTranscript && (
        <div className="user-bubble interim">
          <span className="sender">YOU </span>
          <span className="message-text">{currentTranscript}</span>
        </div>
      )}
      </div>
    </div>
  );
};

export default ChatInterface;
