/**
 * Empty State Component
 * Beautiful empty state shown when user has no tasks
 */

'use client';

import { CheckCircle2, Sparkles } from 'lucide-react';
import { motion } from 'motion/react';

interface EmptyStateProps {
  onCreateClick?: () => void;
}

export function EmptyState({ onCreateClick }: EmptyStateProps) {
  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-[60vh] px-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Illustration Area */}
      <motion.div
        className="relative mb-6"
        animate={{
          y: [0, -10, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        {/* Main Icon */}
        <div className="relative">
          <CheckCircle2 className="h-24 w-24 sm:h-32 sm:w-32 text-gray-300 dark:text-gray-700" />
          {/* Sparkle Accent */}
          <motion.div
            animate={{
              rotate: [0, 360],
              scale: [1, 1.2, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          >
            <Sparkles className="absolute -top-2 -right-2 h-8 w-8 text-yellow-400" />
          </motion.div>
        </div>
      </motion.div>

      {/* Message */}
      <div className="text-center space-y-3 max-w-md">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">
          Your canvas awaits
        </h2>
        <p className="text-base sm:text-lg text-gray-600 dark:text-gray-400">
          No tasks yet. Create your first task to get started on your productivity journey!
        </p>
      </div>

      {/* Optional CTA - will be wired up in Phase 4 */}
      {onCreateClick && (
        <button
          onClick={onCreateClick}
          className="mt-8 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
        >
          Create Your First Task
        </button>
      )}

      {/* Decorative Background */}
      <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200/20 dark:bg-blue-900/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-200/20 dark:bg-purple-900/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.2, 0.25, 0.2],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: 0.5,
          }}
        />
      </div>
    </motion.div>
  );
}
