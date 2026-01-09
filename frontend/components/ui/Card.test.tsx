import React from 'react';
import { render, screen } from '@testing-library/react';
import { Card } from '@/components/ui/Card';

describe('Card Component', () => {
  test('renders card with header, body, and footer', () => {
    render(
      <Card
        header={<div data-testid="header">Header</div>}
        footer={<div data-testid="footer">Footer</div>}
      >
        <div data-testid="body">Body Content</div>
      </Card>
    );

    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('body')).toBeInTheDocument();
    expect(screen.getByTestId('footer')).toBeInTheDocument();
  });

  test('renders card with default variant', () => {
    render(<Card>Content</Card>);
    const card = screen.getByRole('region');
    expect(card).toHaveClass('bg-white', 'border-gray-200', 'dark:bg-gray-800', 'dark:border-gray-700');
  });

  test('renders card with elevated variant', () => {
    render(<Card variant="elevated">Content</Card>);
    const card = screen.getByRole('region');
    expect(card).toHaveClass('shadow-md');
  });

  test('applies custom className', () => {
    render(<Card className="custom-class">Content</Card>);
    const card = screen.getByRole('region');
    expect(card).toHaveClass('custom-class');
  });

  test('renders with custom element type', () => {
    render(<Card as="section">Content</Card>);
    const card = screen.getByRole('region');
    expect(card.tagName).toBe('SECTION');
  });
});