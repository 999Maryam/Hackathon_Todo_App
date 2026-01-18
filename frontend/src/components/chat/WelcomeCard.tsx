'use client';

import { Bot, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

interface WelcomeCardProps {
  onPromptClick: (prompt: string) => void;
}

const examplePrompts = [
  'Add a task to buy groceries',
  'Show me pending tasks',
  'Mark task #1 as complete',
  'Delete completed tasks',
  'What tasks do I have today?',
  'Create a task to call mom',
];

export function WelcomeCard({ onPromptClick }: WelcomeCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center justify-center text-center px-4 py-8 max-w-2xl mx-auto"
    >
      {/* Icon */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
        className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mb-6 shadow-xl shadow-purple-500/30"
      >
        <Bot className="w-10 h-10 text-white" />
      </motion.div>

      {/* Heading */}
      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-3"
      >
        How can I help you today?
      </motion.h2>

      {/* Description */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-gray-500 dark:text-gray-400 mb-8 max-w-md"
      >
        Chat with AI to manage your tasks using natural language. Try one of these examples:
      </motion.p>

      {/* Example Prompts */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex flex-wrap justify-center gap-3"
      >
        {examplePrompts.map((prompt, index) => (
          <motion.button
            key={prompt}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 + index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onPromptClick(prompt)}
            className="px-4 py-2.5 rounded-full border-2 border-purple-200 dark:border-purple-800 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm text-sm font-medium text-purple-700 dark:text-purple-300 hover:bg-purple-50 dark:hover:bg-purple-900/30 hover:border-purple-300 dark:hover:border-purple-700 transition-all duration-200 flex items-center gap-2 shadow-sm hover:shadow-md"
          >
            <Sparkles className="w-3.5 h-3.5" />
            {prompt}
          </motion.button>
        ))}
      </motion.div>
    </motion.div>
  );
}
