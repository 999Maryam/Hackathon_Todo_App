/**
 * Chat input component for Todo AI Chatbot.
 *
 * Task: T021 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-012-FR-015
 */
import { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = () => {
    if (inputValue.trim() && !disabled) {
      onSend(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    } else if (e.key === 'Escape') {
      setInputValue('');
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={disabled ? "Processing..." : "Type a message..."}
        disabled={disabled}
        className={`
          flex-1 rounded-full px-4 py-3 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500
          ${disabled ? 'bg-gray-100 text-gray-500' : 'bg-white text-gray-900'}
        `}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !inputValue.trim()}
        className={`
          rounded-full px-6 py-3 font-medium transition-colors
          ${disabled || !inputValue.trim()
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600'
          }
        `}
      >
        Send
      </button>
    </div>
  );
}