/**
 * Typing indicator component for Todo AI Chatbot.
 *
 * Task: T025 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-016-FR-018
 */

export default function TypingIndicator() {
  return (
    <div className="flex items-center space-x-1.5">
      <div
        className="w-2 h-2 bg-purple-400 dark:bg-purple-500 rounded-full animate-bounce"
        style={{ animationDelay: '0ms', animationDuration: '0.6s' }}
      />
      <div
        className="w-2 h-2 bg-purple-400 dark:bg-purple-500 rounded-full animate-bounce"
        style={{ animationDelay: '150ms', animationDuration: '0.6s' }}
      />
      <div
        className="w-2 h-2 bg-purple-400 dark:bg-purple-500 rounded-full animate-bounce"
        style={{ animationDelay: '300ms', animationDuration: '0.6s' }}
      />
    </div>
  );
}
