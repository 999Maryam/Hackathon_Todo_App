/**
 * Chat bubble component for Todo AI Chatbot.
 *
 * Task: T020 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-010-FR-011
 */
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cn } from '@/lib/utils';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export default function ChatBubble({ role, content, timestamp }: ChatBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={cn('flex gap-3', isUser ? 'flex-row-reverse' : 'flex-row')}>
      {/* Avatar */}
      <div
        className={cn(
          'flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center',
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg shadow-purple-500/20'
            : 'bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
        )}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-purple-600 dark:text-purple-400" />
        )}
      </div>

      {/* Message */}
      <div
        className={cn(
          'max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3',
          isUser
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-tr-sm shadow-lg shadow-purple-500/20'
            : 'bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-gray-800 dark:text-gray-200 rounded-tl-sm shadow-sm'
        )}
      >
        <div
          className={cn(
            'prose prose-sm max-w-none',
            isUser
              ? 'prose-invert'
              : 'dark:prose-invert prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-headings:text-gray-900 dark:prose-headings:text-white prose-strong:text-gray-900 dark:prose-strong:text-white prose-code:text-purple-600 dark:prose-code:text-purple-400 prose-code:bg-purple-50 dark:prose-code:bg-purple-900/30 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none'
          )}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </div>

        {timestamp && (
          <div
            className={cn(
              'text-[10px] mt-2 font-medium',
              isUser ? 'text-purple-200' : 'text-gray-400 dark:text-gray-500'
            )}
          >
            {new Date(timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        )}
      </div>
    </div>
  );
}
