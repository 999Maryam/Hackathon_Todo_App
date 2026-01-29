"use client";

/**
 * Chat page for Todo AI Chatbot.
 *
 * Task: T019 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-009-FR-023
 */
import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { ChatBubble, TypingIndicator } from '@/components';
import { chatApi, ToolCallRecord } from '@/lib/api';
import { ChatLayout } from '@/components/layout/ChatLayout';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { WelcomeCard } from '@/components/chat/WelcomeCard';
import { Button } from '@/components/ui/button';

interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  tool_calls?: ToolCallRecord[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/sign-in');
    }
  }, [authLoading, isAuthenticated, router]);

  // Load conversation from localStorage on mount
  useEffect(() => {
    if (user?.id) {
      const storedConversations = localStorage.getItem('chat_conversations');
      if (storedConversations) {
        const conversations = JSON.parse(storedConversations);
        const userConversations = conversations[user.id] || [];
        setMessages(userConversations);
      }
    }
  }, [user?.id]);

  // Save conversation to localStorage whenever messages change
  useEffect(() => {
    if (user?.id && messages.length > 0) {
      const storedConversations = localStorage.getItem('chat_conversations');
      const conversations = storedConversations ? JSON.parse(storedConversations) : {};
      conversations[user.id] = messages;
      localStorage.setItem('chat_conversations', JSON.stringify(conversations));
    }
  }, [messages, user?.id]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (messagesEndRef.current?.scrollIntoView) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading || !user?.id) return;

    // Clear input
    setInputValue('');

    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send to API
      const response = await chatApi.sendMessage(user.id, {
        message: text,
        conversation_id: undefined // Will create new conversation
      });

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    if (user?.id) {
      const storedConversations = localStorage.getItem('chat_conversations');
      if (storedConversations) {
        const conversations = JSON.parse(storedConversations);
        delete conversations[user.id];
        localStorage.setItem('chat_conversations', JSON.stringify(conversations));
      }
    }
  };

  const handlePromptClick = (prompt: string) => {
    setInputValue(prompt);
    inputRef.current?.focus();
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage(inputValue);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 via-white to-purple-50/30 dark:from-gray-950 dark:via-gray-900 dark:to-purple-950/20">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <ChatLayout>
      <div className="flex flex-col h-screen">
        {/* Header */}
        <ChatHeader onClearChat={handleClearChat} />

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto">
          <AnimatePresence mode="wait">
            {messages.length === 0 ? (
              <motion.div
                key="welcome"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full flex items-center justify-center pt-8 pb-32"
              >
                <WelcomeCard onPromptClick={handlePromptClick} />
              </motion.div>
            ) : (
              <motion.div
                key="messages"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="max-w-4xl mx-auto px-4 lg:px-6 py-6 space-y-4 pb-32"
              >
                {messages.map((msg, index) => (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <ChatBubble
                      role={msg.role}
                      content={msg.content}
                      timestamp={msg.timestamp}
                    />
                  </motion.div>
                ))}

                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 shadow-sm border border-gray-100 dark:border-gray-700">
                      <TypingIndicator />
                    </div>
                  </motion.div>
                )}

                <div ref={messagesEndRef} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Input Bar - Fixed at bottom */}
        <div className="sticky bottom-0 bg-gradient-to-t from-white via-white to-white/80 dark:from-gray-900 dark:via-gray-900 dark:to-gray-900/80 backdrop-blur-xl border-t border-gray-200/50 dark:border-gray-800/50 px-4 lg:px-6 py-4">
          <form
            onSubmit={handleSubmit}
            className="max-w-4xl mx-auto"
          >
            <div className="relative flex items-center gap-3">
              <div className="flex-1 relative">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type a message..."
                  disabled={isLoading}
                  className="w-full px-5 py-3.5 pr-14 rounded-2xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-purple-400 dark:focus:border-purple-500 focus:ring-4 focus:ring-purple-100 dark:focus:ring-purple-900/30 transition-all duration-200 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <Button
                  type="submit"
                  disabled={isLoading || !inputValue.trim()}
                  size="icon"
                  className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg shadow-purple-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                  data-testid="send-button"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
            <p className="text-xs text-center text-gray-400 dark:text-gray-500 mt-3">
              AI can make mistakes. Please verify important information.
            </p>
          </form>
        </div>
      </div>
    </ChatLayout>
  );
}
