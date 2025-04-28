'use client';

import React from 'react';
import { FaSignOutAlt, FaTimes, FaToggleOn, FaToggleOff } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';

interface ChatSidebarProps {
  isMobile: boolean;
  isOpen: boolean;
  onClose: () => void;
}

export default function ChatSidebar({ isMobile, isOpen, onClose }: ChatSidebarProps) {
  const { logout, user } = useAuth();
  const { useRag, setUseRag, messages } = useChat();
  
  // Group messages by date (simplified version - could be enhanced)
  const messageGroups = React.useMemo(() => {
    const groups: Record<string, string[]> = {};
    
    // Extract unique first sentences from user messages
    messages.forEach(msg => {
      if (msg.role === 'user') {
        const firstLine = msg.content.split('\n')[0].substring(0, 30) + (msg.content.length > 30 ? '...' : '');
        if (!Object.values(groups).flat().includes(firstLine)) {
          const date = new Date().toLocaleDateString(); // In a real app, you'd store timestamps with messages
          groups[date] = groups[date] || [];
          groups[date].push(firstLine);
        }
      }
    });
    
    return groups;
  }, [messages]);

  if (isMobile && !isOpen) return null;

  return (
    <div className={`
      bg-gray-900 text-white
      ${isMobile 
        ? 'fixed inset-y-0 left-0 z-40 w-64 transform transition-transform ease-in-out duration-300 ' + 
          (isOpen ? 'translate-x-0' : '-translate-x-full')
        : 'sticky top-0 h-screen w-64 flex-shrink-0'
      }
    `}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-800">
        <h2 className="text-xl font-bold">Huberman RAG</h2>
        {isMobile && (
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-white"
          >
            <FaTimes />
          </button>
        )}
      </div>
      
      {/* User info */}
      <div className="p-4 border-b border-gray-800">
        <div className="flex justify-between items-center">
          <div className="truncate">{user?.email}</div>
          <button 
            onClick={logout}
            className="text-gray-400 hover:text-white"
            aria-label="Logout"
          >
            <FaSignOutAlt />
          </button>
        </div>
      </div>
      
      {/* RAG Toggle */}
      <div className="p-4 border-b border-gray-800">
        <div 
          className="flex items-center justify-between cursor-pointer"
          onClick={() => setUseRag(!useRag)}
        >
          <span>Use RAG</span>
          <div className="text-xl">
            {useRag ? <FaToggleOn className="text-huberman-secondary" /> : <FaToggleOff className="text-gray-400" />}
          </div>
        </div>
      </div>
      
      {/* Chat history */}
      <div className="overflow-y-auto h-[calc(100vh-200px)] p-4">
        <h3 className="text-sm uppercase text-gray-400 mb-2">Recent Conversations</h3>
        {Object.entries(messageGroups).map(([date, queries], groupIndex) => (
          <div key={groupIndex} className="mb-4">
            <h4 className="text-xs text-gray-500 mb-1">{date}</h4>
            <ul>
              {queries.map((query, index) => (
                <li 
                  key={index}
                  className="py-2 px-3 rounded hover:bg-gray-800 cursor-pointer mb-1 text-sm truncate"
                >
                  {query}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
} 