'use client';

import React, { forwardRef, InputHTMLAttributes } from 'react';

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'id'> {
  /**
   * Type of input element
   */
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'date' | 'time' | 'datetime-local';
  /**
   * Label for the input field
   */
  label?: string;
  /**
   * Placeholder text for the input field
   */
  placeholder?: string;
  /**
   * Error message to display when input is invalid
   */
  error?: string;
  /**
   * Whether the input field is disabled
   */
  disabled?: boolean;
  /**
   * Additional CSS classes to apply
   */
  className?: string;
  /**
   * ID for the input field (required for accessibility)
   */
  id: string;
  /**
   * Whether the input field is required
   */
  required?: boolean;
}

/**
 * A reusable Input component with support for various input types, labels,
 * error states, and accessibility features.
 */
const Input = forwardRef<HTMLInputElement, InputProps>(({
  type = 'text',
  label,
  placeholder,
  error,
  disabled = false,
  className = '',
  id,
  required = false,
  ...props
}, ref) => {
  const hasError = Boolean(error);

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={id}
          className={`block text-sm font-medium mb-1 ${
            disabled
              ? 'text-gray-400 dark:text-gray-500'
              : 'text-gray-700 dark:text-gray-200'
          }`}
        >
          {label} {required && <span className="text-red-500" aria-label="required">*</span>}
        </label>
      )}

      <input
        id={id}
        type={type}
        placeholder={placeholder}
        disabled={disabled}
        ref={ref}
        aria-invalid={hasError}
        aria-describedby={hasError ? `${id}-error` : undefined}
        required={required}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          transition-colors duration-200
          ${disabled
            ? 'bg-gray-100 border-gray-300 text-gray-500 cursor-not-allowed dark:bg-gray-700 dark:border-gray-600 dark:text-gray-400'
            : 'bg-white border-gray-300 text-gray-900 hover:border-gray-400 dark:bg-gray-800 dark:border-gray-600 dark:text-white'
          }
          ${hasError
            ? 'border-red-500 focus:ring-red-500 focus:border-red-500 dark:border-red-400 dark:focus:ring-red-400 dark:focus:border-red-400'
            : ''
          }
          ${className}
        `}
        {...props}
      />

      {hasError && (
        <p
          id={`${id}-error`}
          className="mt-1 text-sm text-red-600 dark:text-red-400"
          role="alert"
          aria-live="polite"
        >
          {error}
        </p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;