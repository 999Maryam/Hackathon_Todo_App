/**
 * Tests for the chat endpoint and UI components
 *
 * Note: These tests require vitest and @testing-library/react to be installed.
 * Run: npm install -D vitest @testing-library/react @testing-library/jest-dom
 */

// Types for mock functions (avoid 'any')
type MockFunction = ReturnType<typeof vi.fn>;

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { useAuth } from '@/hooks/useAuth';
import { chatApi } from '@/lib/api';
import ChatPage from '@/app/chat/page';

// Mock the Next.js router
vi.mock('next/navigation', async () => {
  const actual = await vi.importActual('next/navigation');
  return {
    ...actual,
    useRouter: () => ({
      push: vi.fn(),
      prefetch: vi.fn(),
    }),
  };
});

// Mock the auth hook
vi.mock('@/hooks/useAuth', () => ({
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
    (useAuth as MockFunction).mockReturnValue({
      user: mockUser,
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      refreshUser: vi.fn(),
    });

    (chatApi.sendMessage as MockFunction).mockResolvedValue({
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
    expect(screen.getByTestId('send-button')).toBeInTheDocument(); // Find the submit button by its test ID
  });

  it('allows sending a message', async () => {
    render(<ChatPage />);

    const input = screen.getByPlaceholderText('Type a message...');
    const sendButton = screen.getByTestId('send-button');

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
    const sendButton = screen.getByTestId('send-button');

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getAllByText('Test message')).toBeTruthy();
      expect(screen.getAllByText('Hello! How can I help you?')).toBeTruthy();
    });
  });

  it('shows loading state when processing', async () => {
    // Mock a delayed response
    (chatApi.sendMessage as MockFunction).mockImplementation(() =>
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
    const sendButton = screen.getByTestId('send-button');

    fireEvent.change(input, { target: { value: 'Loading test' } });
    fireEvent.click(sendButton);

    // Check that loading state is shown (TypingIndicator)
    await waitFor(() => {
      expect(screen.getByTestId('typing-indicator')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getAllByText('Delayed response')).toBeTruthy();
    });
  });
});

// Note: Chat component tests removed - ChatBubble, ChatInput, TypingIndicator
// are internal components of ChatPage and should be tested via integration tests