'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { useAuth } from './context/AuthContext';
import LoginModal from './components/LoginModal';

export default function Home() {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && !loading) {
      router.push('/chat');
    }
  }, [isAuthenticated, loading, router]);

  return (
    <div className="bg-huberman-light min-h-screen flex flex-col">
      <main className="flex-grow flex flex-col items-center justify-center p-6">
        <div className="text-center max-w-4xl">
          <div className="flex justify-center mb-6">
            <Image 
              src="/images/HUBLAB_banner.jpg" 
              alt="Huberman Lab" 
              width={600} 
              height={200}
              className="rounded-lg shadow-lg"
            />
          </div>
          
          <h1 className="text-4xl font-bold text-huberman-dark mb-4">
            Huberman Lab AI Assistant
          </h1>
          
          <p className="text-xl text-gray-700 mb-8">
            Ask questions about Dr. Andrew Huberman's teachings and get accurate, science-based answers.
          </p>
          
          <button
            onClick={() => setShowLoginModal(true)}
            className="bg-huberman-primary text-white py-3 px-8 rounded-full text-lg font-medium hover:bg-opacity-90 transition-colors shadow-lg"
          >
            Get Started
          </button>
        </div>
      </main>
      
      <footer className="py-6 text-center text-gray-600 border-t">
        <p>Powered by RAG technology with Huberman Lab content</p>
      </footer>

      <LoginModal 
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
      />
    </div>
  );
}
