// frontend/src/components/chat.js
import React, { useState } from 'react';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    const newMessage = { text: input, sender: 'user' };
    setMessages([...messages, newMessage]);

    const response = await fetch('/api/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: input }),
    });

    const data = await response.json();
    const botMessage = { text: data.answer, sender: 'bot' };
    setMessages([...messages, newMessage, botMessage]);

    setInput('');
  };

  return (
    <div>
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your question..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chat;