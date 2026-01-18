/**
 * Tests for the chat endpoint and UI components
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';
import { chatApi } from '@/lib/api';
import ChatPage from '@/app/chat/page';

// Mock the auth hook
vi.mock('better-auth/react', () => ({
  useAuth: vi.fn(),
}));

// Mock the chat API
vi.mock('@/lib/api', () => ({
  chatApi: {
    sendMessage: vi.fn(),
  },
}));

describe('ChatPage', () => {
  const mockUser = {
    id: 'test-user-id',
    email: 'test@example.com',
    name: 'Test User',
  };

  beforeEach(() => {
    (useAuth as any).mockReturnValue({
      user: mockUser,
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      refreshUser: vi.fn(),
    });

    (chatApi.sendMessage as any).mockResolvedValue({
      conversation_id: 1,
      response: 'Hello! How can I help you?',
      tool_calls: [],
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders the chat page with header and input', () => {
    render(<ChatPage />);

    expect(screen.getByText('AI Task Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type a message...')).toBeInTheDocument();
    expect(screen.getByText('Send')).toBeInTheDocument();
  });

  it('allows sending a message', async () => {
    render(<ChatPage />);

    const input = screen.getByPlaceholderText('Type a message...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(chatApi.sendMessage).toHaveBeenCalledWith('test-user-id', {
        message: 'Hello!',
        conversation_id: undefined,
      });
    });
  });

  it('displays user and assistant messages', async () => {
    render(<ChatPage />);

    const input = screen.getByPlaceholderText('Type a message...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
      expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });
  });

  it('shows loading state when processing', async () => {
    // Mock a delayed response
    (chatApi.sendMessage as any).mockImplementation(() =>
      new Promise(resolve =>
        setTimeout(() => resolve({
          conversation_id: 1,
          response: 'Delayed response',
          tool_calls: [],
        }), 100)
      )
    );

    render(<ChatPage />);

    const input = screen.getByPlaceholderText('Type a message...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Loading test' } });
    fireEvent.click(sendButton);

    // Check that loading state is shown
    expect(screen.getByText('Processing...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Delayed response')).toBeInTheDocument();
    });
  });
});

describe('Chat Components', () => {
  it('ChatBubble renders user and assistant messages differently', () => {
    const { container: userBubble } = render(
      <ChatBubble role="user" content="User message" />
    );
    const { container: assistantBubble } = render(
      <ChatBubble role="assistant" content="Assistant message" />
    );

    // User bubble should have gradient styling
    expect(userBubble.querySelector('div')).toHaveClass(expect.stringContaining('from-blue-500'));

    // Assistant bubble should have white background
    expect(assistantBubble.querySelector('div')).toHaveClass(expect.stringContaining('bg-white'));
  });

  it('ChatInput handles keyboard events', () => {
    const mockOnSend = vi.fn();
    const { getByRole } = render(
      <ChatInput onSend={mockOnSend} />
    );

    const input = getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Test message' } });

    // Simulate Enter key press
    fireEvent.keyDown(input, { key: 'Enter', shiftKey: false });

    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });

  it('TypingIndicator shows animated dots', () => {
    const { container } = render(<TypingIndicator />);
    const dots = container.querySelectorAll('.animate-bounce');
    expect(dots).toHaveLength(3);
  });
});