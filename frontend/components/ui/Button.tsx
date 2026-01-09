'use client';

import React, { ButtonHTMLAttributes, forwardRef } from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Variant of the button
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  /**
   * Size of the button
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';
  /**
   * Whether the button is in loading state
   * @default false
   */
  isLoading?: boolean;
  /**
   * Children content of the button
   */
  children: React.ReactNode;
}

/**
 * Professional, responsive Button component for the todo app
 * Supports different variants, sizes, and loading states
 * Fully accessible with proper ARIA attributes
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', isLoading = false, children, className = '', disabled, ...props }, ref) => {
    // Base classes
    const baseClasses = [
      'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
    ];

    // Variant classes
    const variantClasses = {
      primary: [
        'bg-blue-600 text-white hover:bg-blue-700',
        'dark:bg-blue-500 dark:hover:bg-blue-600',
      ],
      secondary: [
        'bg-gray-200 text-gray-900 hover:bg-gray-300',
        'dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600',
      ],
      outline: [
        'border border-gray-300 bg-transparent hover:bg-gray-100 text-gray-700',
        'dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800',
      ],
      ghost: [
        'hover:bg-gray-100 text-gray-700',
        'dark:text-gray-300 dark:hover:bg-gray-800',
      ],
      destructive: [
        'bg-red-600 text-white hover:bg-red-700',
        'dark:bg-red-500 dark:hover:bg-red-600',
      ],
    };

    // Size classes
    const sizeClasses = {
      sm: 'h-9 px-3 py-2 text-xs',
      md: 'h-10 px-4 py-2 text-sm',
      lg: 'h-11 px-8 py-3 text-base',
    };

    // Combine all classes
    const classes = [
      ...baseClasses,
      ...variantClasses[variant],
      sizeClasses[size],
      className,
    ].join(' ');

    return (
      <button
        ref={ref}
        className={classes}
        disabled={disabled || isLoading}
        aria-disabled={disabled || isLoading}
        data-loading={isLoading}
        {...props}
      >
        {isLoading && (
          <span
            className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
            aria-hidden="true"
          />
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;