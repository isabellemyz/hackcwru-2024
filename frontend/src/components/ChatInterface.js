import React from 'react';

const ChatInterface = ({ messages }) => {
  return (
    <div className="flex flex-col items-center p-4 bg-white shadow rounded">
      <div className="overflow-auto h-96 w-full p-2">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>{msg.text}</div>
        ))}
      </div>
    </div>
  );
};

export default ChatInterface;
