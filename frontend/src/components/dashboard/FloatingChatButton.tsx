'use client';

import { useRouter } from 'next/navigation';
import { MessageSquare, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export function FloatingChatButton() {
  const router = useRouter();

  return (
    <motion.button
      onClick={() => router.push('/chat')}
      className="fixed bottom-6 right-24 z-50 group"
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      {/* Pulse ring animation */}
      <span className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 animate-ping opacity-25" />

      {/* Button */}
      <div className="relative flex items-center gap-2 px-5 py-3.5 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-300">
        <MessageSquare className="w-5 h-5" />
        <span className="hidden sm:inline">AI Chat</span>
        <Sparkles className="w-4 h-4 text-yellow-300 animate-pulse" />
      </div>

      {/* Tooltip on hover */}
      <div className="absolute bottom-full right-0 mb-2 px-3 py-1.5 rounded-lg bg-gray-900 dark:bg-gray-700 text-white text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
        Chat with AI Assistant
        <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900 dark:border-t-gray-700" />
      </div>
    </motion.button>
  );
}
