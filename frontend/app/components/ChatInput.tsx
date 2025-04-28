'use client';

import React, { useState, FormEvent } from 'react';
import { FaPaperPlane } from 'react-icons/fa';
import { useChat } from '../context/ChatContext';

export default function ChatInput() {
  const [message, setMessage] = useState('');
  const { sendMessage, loading, useRag } = useChat();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    if (!message.trim() || loading) return;
    
    try {
      await sendMessage(message, useRag);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative flex items-center">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask about Dr. Huberman's teachings..."
        className="w-full rounded-full bg-gray-800 border border-gray-700 py-3 pl-4 pr-12 text-white placeholder-gray-400 focus:border-huberman-secondary focus:ring focus:ring-huberman-secondary focus:ring-opacity-50"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !message.trim()}
        className={`absolute right-2 rounded-full p-2 ${
          loading || !message.trim() 
            ? 'bg-gray-700 text-gray-400' 
            : 'bg-huberman-primary text-white hover:bg-opacity-90'
        } transition-colors`}
      >
        <FaPaperPlane />
      </button>
    </form>
  );
} 