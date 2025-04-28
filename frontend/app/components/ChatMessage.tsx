'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '../context/ChatContext';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex w-full my-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] px-4 py-3 rounded-lg ${
          isUser 
            ? 'bg-huberman-primary text-white rounded-br-none' 
            : 'bg-gray-700 text-gray-100 rounded-bl-none'
        }`}
      >
        <div className="markdown-content">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              // Style headings
              h1: ({...props}) => <h1 className="text-xl font-bold my-2" {...props} />,
              h2: ({...props}) => <h2 className="text-lg font-bold my-2" {...props} />,
              h3: ({...props}) => <h3 className="text-md font-bold my-1" {...props} />,
              // Style lists
              ul: ({...props}) => <ul className="list-disc pl-5 my-2" {...props} />,
              ol: ({...props}) => <ol className="list-decimal pl-5 my-2" {...props} />,
              // Style links
              a: ({...props}) => <a className="text-huberman-secondary underline" {...props} />,
              // Style code - using a simpler approach
              code: ({...props}) => <code className="bg-black bg-opacity-20 px-1 py-0.5 rounded text-sm" {...props} />,
              pre: ({...props}) => <pre className="bg-black bg-opacity-30 p-2 rounded-md my-2 overflow-x-auto text-sm" {...props} />,
              // Style blockquotes
              blockquote: ({...props}) => <blockquote className="border-l-4 border-gray-500 pl-4 italic my-2" {...props} />,
              // Add bottom margin to paragraphs for better spacing except for the last one
              p: ({...props}) => <p className="mb-2 last:mb-0" {...props} />
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
} 