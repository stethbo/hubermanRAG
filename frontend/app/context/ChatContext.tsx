'use client';

import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { chatService } from '../services/api';
import { useAuth } from './AuthContext';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatContextType {
  messages: Message[];
  sendMessage: (message: string, useRag: boolean) => Promise<void>;
  loading: boolean;
  useRag: boolean;
  setUseRag: (value: boolean) => void;
}

const ChatContext = createContext<ChatContextType>({
  messages: [],
  sendMessage: async () => {},
  loading: false,
  useRag: true,
  setUseRag: () => {},
});

export const useChat = () => useContext(ChatContext);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [useRag, setUseRag] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchChatHistory();
    }
  }, [isAuthenticated]);

  const fetchChatHistory = async () => {
    try {
      setLoading(true);
      const history = await chatService.getChatHistory();
      setMessages(history);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (message: string, useRag: boolean) => {
    try {
      setLoading(true);
      
      // Optimistically update UI with user message
      const userMessage: Message = { role: 'user', content: message };
      setMessages((prev) => [...prev, userMessage]);
      
      // Send message to API
      const response = await chatService.sendMessage(message, useRag);
      
      // Update all messages with response from server
      setMessages(response.chat_history);
    } catch (error) {
      console.error('Error sending message:', error);
      // Revert optimistic update on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{ 
      messages, 
      sendMessage, 
      loading,
      useRag,
      setUseRag
    }}>
      {children}
    </ChatContext.Provider>
  );
}; 