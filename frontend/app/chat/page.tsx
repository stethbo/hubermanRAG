'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FaBars } from 'react-icons/fa';
import Image from 'next/image';
import { useAuth } from '../context/AuthContext';
import { ChatProvider } from '../context/ChatContext';
import ChatSidebar from '../components/ChatSidebar';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import { useChat } from '../context/ChatContext';

// Chat display component (separate to use context)
function ChatDisplay() {
  const { messages, loading } = useChat();
  
  return (
    <div className="flex-1 overflow-y-auto p-4">
      {messages.length === 0 && !loading ? (
        <div className="h-full flex flex-col items-center justify-center text-gray-300">
          <div className="mb-6">
            <Image 
              src="/images/HUBLAB_banner.jpg" 
              alt="Huberman Lab" 
              width={1000} 
              height={200}
              className="rounded-lg"
            />
          </div>
          <p className="text-xl font-semibold mb-2">Welcome to Huberman RAG Chat</p>
          <p>Ask a question about Dr. Huberman's teachings to get started</p>
        </div>
      ) : (
        <div className="space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {loading && (
            <div className="flex justify-center my-4">
              <div className="animate-pulse text-huberman-secondary">
                Processing...
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function ChatPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-huberman-dark text-white">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect due to the effect
  }

  return (
    <ChatProvider>
      <div className="flex flex-col h-screen bg-huberman-dark text-white">
        <div className="flex flex-1 overflow-hidden">
          {/* Sidebar for desktop */}
          <ChatSidebar
            isMobile={false}
            isOpen={true}
            onClose={() => {}}
          />
          
          {/* Mobile sidebar */}
          <ChatSidebar
            isMobile={true}
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
          />
          
          {/* Main content */}
          <div className="flex-1 flex flex-col">
            {/* Header */}
            <header className="bg-huberman-dark border-b border-gray-700 p-4 md:hidden">
              <button
                onClick={() => setSidebarOpen(true)}
                className="text-gray-300 hover:text-white"
              >
                <FaBars />
              </button>
            </header>
            
            {/* Chat area */}
            <div className="flex-1 flex flex-col overflow-hidden">
              <ChatDisplay />
              
              {/* Chat input */}
              <div className="p-4 border-t border-gray-700">
                <ChatInput />
              </div>
            </div>
          </div>
        </div>
      </div>
    </ChatProvider>
  );
} 