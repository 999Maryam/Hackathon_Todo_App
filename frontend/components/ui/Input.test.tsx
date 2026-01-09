import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Input from '@/components/ui/Input';

describe('Input Component', () => {
  const defaultProps = {
    id: 'test-input',
    label: 'Test Label',
    placeholder: 'Test Placeholder',
  };

  it('renders without crashing', () => {
    render(<Input {...defaultProps} />);
    expect(screen.getByLabelText('Test Label')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Test Placeholder')).toBeInTheDocument();
  });

  it('displays the correct input type', () => {
    render(<Input {...defaultProps} type="email" />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toHaveAttribute('type', 'email');
  });

  it('applies disabled state correctly', () => {
    render(<Input {...defaultProps} disabled={true} />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toBeDisabled();
    expect(inputElement).toHaveClass('cursor-not-allowed');
  });

  it('shows error message when error prop is provided', () => {
    render(<Input {...defaultProps} error="This is an error" />);
    expect(screen.getByText('This is an error')).toBeInTheDocument();
    expect(screen.getByRole('alert')).toBeInTheDocument();
  });

  it('does not show error message when no error prop is provided', () => {
    render(<Input {...defaultProps} />);
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('has proper ARIA attributes when error is present', () => {
    render(<Input {...defaultProps} error="Error message" />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toHaveAttribute('aria-invalid', 'true');
    expect(inputElement).toHaveAttribute('aria-describedby', 'test-input-error');
  });

  it('has proper ARIA attributes when no error is present', () => {
    render(<Input {...defaultProps} />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toHaveAttribute('aria-invalid', 'false');
    expect(inputElement).not.toHaveAttribute('aria-describedby');
  });

  it('handles change events properly', () => {
    const mockOnChange = jest.fn();
    render(<Input {...defaultProps} onChange={mockOnChange} />);

    const inputElement = screen.getByLabelText('Test Label');
    fireEvent.change(inputElement, { target: { value: 'test value' } });

    expect(mockOnChange).toHaveBeenCalledTimes(1);
    expect(inputElement).toHaveValue('test value');
  });

  it('applies required attribute when specified', () => {
    render(<Input {...defaultProps} required={true} />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toBeRequired();
    expect(screen.getByText('*')).toBeInTheDocument(); // Required indicator
  });

  it('renders different input types correctly', () => {
    const types = ['text', 'email', 'password', 'number', 'tel', 'url', 'search', 'date', 'time', 'datetime-local'];

    types.forEach(type => {
      render(<Input id={`input-${type}`} type={type} />);
      const inputElement = screen.getByRole('textbox', { hidden: true }) ||
                          screen.getByLabelText('', { selector: `input[type="${type}"]` }) ||
                          document.getElementById(`input-${type}`);

      if (inputElement) {
        expect(inputElement).toHaveAttribute('type', type);
      }
    });
  });

  it('applies additional CSS classes when className prop is provided', () => {
    render(<Input {...defaultProps} className="custom-class another-class" />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toHaveClass('custom-class', 'another-class');
  });

  it('forwards ref properly', () => {
    const ref = React.createRef<HTMLInputElement>();
    render(<Input {...defaultProps} ref={ref} />);

    expect(ref.current).toBeInTheDocument();
    expect(ref.current).toBeInstanceOf(HTMLInputElement);
  });

  it('does not render label when label prop is not provided', () => {
    render(<Input id="no-label-input" placeholder="No label" />);
    expect(screen.queryByText('Test Label')).not.toBeInTheDocument();
    expect(screen.getByPlaceholderText('No label')).toBeInTheDocument();
  });

  it('has proper focus ring styles', () => {
    render(<Input {...defaultProps} />);
    const inputElement = screen.getByLabelText('Test Label');
    inputElement.focus();
    expect(inputElement).toHaveFocus();
    expect(inputElement).toHaveClass('focus:ring-2', 'focus:ring-blue-500', 'focus:border-blue-500');
  });

  it('has proper error state styles', () => {
    render(<Input {...defaultProps} error="Error message" />);
    const inputElement = screen.getByLabelText('Test Label');
    expect(inputElement).toHaveClass('border-red-500', 'focus:ring-red-500', 'focus:border-red-500');
  });
});