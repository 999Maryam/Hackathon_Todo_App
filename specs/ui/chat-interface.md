# UI Design Guidelines: Chat Interface for Todo AI Chatbot

**Feature**: 008-chat-endpoint-ui
**Date**: 2026-01-15

---

## Visual Design

### Color Palette
- **Primary Gradient (User Messages)**: `from-blue-500 to-purple-600` (#3B82F6 to #9333EA)
- **Assistant Messages**: `bg-white border-gray-200` (#FFFFFF with #E5E7EB border)
- **Background**: `from-gray-50 to-gray-100` (#F9FAFB to #F3F4F6)
- **Text**: `text-gray-800` (#1F2937) for content, `text-white` (#FFFFFF) for user bubbles

### Typography
- **Font Family**: System default with Tailwind's sans-serif stack
- **Message Text**: Base size with responsive scaling (sm on mobile, base on desktop)
- **Header**: Medium weight for clear hierarchy
- **Timestamps**: Small, light text with reduced opacity

### Spacing & Layout
- **Message bubbles**: 1rem vertical padding, 1rem horizontal padding
- **Between messages**: 1rem vertical spacing
- **Container padding**: 1rem on sides, 1rem top/bottom for messages area
- **Mobile responsiveness**: 80% width max, 70% on desktop

---

## Component Specifications

### ChatBubble Component
```tsx
interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}
```

**User Bubble (Right-aligned)**:
- Background: Gradient from blue-500 to purple-600
- Text: White
- Rounded corners: Default with `rounded-br-none` to maintain speech bubble shape
- Alignment: Flex-end (right-aligned)

**Assistant Bubble (Left-aligned)**:
- Background: White
- Border: 1px solid gray-200
- Text: Gray-800
- Rounded corners: Default with `rounded-bl-none` to maintain speech bubble shape
- Alignment: Flex-start (left-aligned)

### ChatInput Component
- **Position**: Fixed/sticky at bottom of screen
- **Height**: Auto-adjusting with minimum height
- **Elements**: Text input field, Send button (paper plane icon)
- **Keyboard Support**: Enter to send, Shift+Enter for new line, Esc to clear
- **Placeholder**: "Type a message to your AI assistant..."

### TypingIndicator Component
- **Animation**: Three bouncing dots with staggered timing
- **Color**: Gray-400 dots
- **Position**: Left-aligned to match assistant messages
- **Duration**: Subtle bounce animation with 0.3s cycle

---

## Animation & Interaction Design

### Message Appearance
- **Animation**: Fade-in + slide-up using Framer Motion
- **Duration**: 0.3 seconds
- **Easing**: Smooth, natural motion
- **Trigger**: On component mount

### Auto-scroll Behavior
- **Timing**: After each new message is rendered
- **Easing**: Gentle, smooth scrolling
- **Behavior**: Always scroll to bottom of message container

### Loading States
- **During AI Processing**: Typing indicator appears
- **During Tool Execution**: Wave animation or spinner
- **Error States**: Friendly error message with retry option

---

## Responsive Design

### Mobile (Up to 640px)
- **Message Width**: 80% of container width
- **Input Bar**: Full width at bottom
- **Font Size**: Slightly smaller for better density
- **Touch Targets**: Minimum 44px for accessibility

### Tablet (641px - 1024px)
- **Message Width**: 75% of container width
- **Layout**: Optimized for both portrait and landscape
- **Touch Targets**: Maintained at accessible size

### Desktop (1025px+)
- **Message Width**: 70% of container width
- **Sidebar**: Potential for conversation history panel
- **Layout**: Wider conversation area with better spacing

---

## Component List

### Core Components
1. **ChatPage** - Main page component with layout structure
2. **ChatBubble** - Message display component with role-based styling
3. **ChatInput** - Input area with send button and keyboard support
4. **TypingIndicator** - Loading animation for AI processing
5. **ChatContainer** - Overall layout and message scroller

### Supporting Components
1. **Header** - Chat header with title and user info
2. **MessageList** - Container for all messages with scroll behavior
3. **InputBar** - Fixed input area at bottom
4. **ErrorMessage** - Error display with user-friendly messaging

---

## User Experience Flows

### New Message Flow
1. User types message in input field
2. User clicks Send button or presses Enter
3. Message appears in UI immediately (optimistic update)
4. Request sent to backend API
5. Typing indicator appears
6. Assistant response received and displayed
7. Auto-scroll to bottom

### Error Handling Flow
1. If API request fails
2. Show error message in assistant bubble
3. Provide option to retry
4. Maintain conversation flow

### Conversation Persistence
1. On page load, check for stored conversation ID
2. If exists, load conversation history
3. If not, start new conversation
4. Store current conversation ID in localStorage
5. On new conversation, clear stored ID

---

## Accessibility Considerations

### ARIA Labels
- Input field: "Chat message input"
- Send button: "Send message"
- Message bubbles: Role-appropriate labeling
- Loading indicators: Proper announcement for screen readers

### Keyboard Navigation
- Tab order: Logical flow through chat interface
- Enter key: Send message
- Escape key: Clear input field
- Arrow keys: Navigate between messages (if needed)

### Color Contrast
- All text meets WCAG AA contrast requirements
- Gradient text has sufficient contrast against background
- Disabled states maintain readability

---

## Performance Optimizations

### Message Rendering
- Virtual scrolling for long conversations (if needed)
- Memoization of message components
- Efficient re-rendering only for new messages

### Asset Loading
- Lazy loading of components not immediately visible
- Optimized icons and animations
- Efficient image handling (if images are added later)

---

## Screenshots Notes

### Expected Screenshots
1. **Desktop View**: Full chat interface with message bubbles
2. **Mobile View**: Optimized mobile chat interface
3. **Loading State**: Typing indicator in action
4. **Error State**: Friendly error message display
5. **Multi-message Conversation**: Several exchanges showing conversation flow

### Key Elements to Capture
- Gradient user message bubbles
- Clean assistant message bubbles with markdown support
- Typing indicator animation
- Responsive input bar at bottom
- Auto-scroll behavior demonstration