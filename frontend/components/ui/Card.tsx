import React from 'react';

export interface CardProps {
  /**
   * The header content of the card
   */
  header?: React.ReactNode;
  /**
   * The main content of the card
   */
  children?: React.ReactNode;
  /**
   * The footer content of the card
   */
  footer?: React.ReactNode;
  /**
   * The variant of the card
   * @default 'default'
   */
  variant?: 'default' | 'elevated';
  /**
   * Additional CSS classes to apply to the card
   */
  className?: string;
  /**
   * The HTML element to render as the card container
   * @default 'div'
   */
  as?: React.ElementType;
  /**
   * Accessibility role for the card
   * @default 'region'
   */
  role?: string;
  /**
   * Optional aria-label for accessibility
   */
  'aria-label'?: string;
  /**
   * Optional aria-labelledby for accessibility
   */
  'aria-labelledby'?: string;
}

/**
 * A responsive Card component with header, body, and footer sections
 */
const Card = React.forwardRef<HTMLDivElement, CardProps>(({
  header,
  children,
  footer,
  variant = 'default',
  className = '',
  as: Component = 'div',
  role = 'region',
  'aria-label': ariaLabel,
  'aria-labelledby': ariaLabelledby,
  ...props
}) => {
  // Determine base styles and variant-specific styles
  const baseStyles = 'rounded-lg border shadow-sm transition-all duration-200 overflow-hidden';
  const variantStyles = variant === 'elevated'
    ? 'bg-white border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700'
    : 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700';

  // Combine all classes
  const cardClassName = `${baseStyles} ${variantStyles} ${className}`.trim();

  return (
    <Component
      className={cardClassName}
      role={role}
      aria-label={ariaLabel}
      aria-labelledby={ariaLabelledby}
      {...props}
    >
      {header && (
        <div className="px-4 py-3 border-b border-gray-100 bg-gray-50 dark:border-gray-700 dark:bg-gray-700/50">
          {header}
        </div>
      )}
      {children && (
        <div className="p-4">
          {children}
        </div>
      )}
      {footer && (
        <div className="px-4 py-3 border-t border-gray-100 bg-gray-50 dark:border-gray-700 dark:bg-gray-700/50">
          {footer}
        </div>
      )}
    </Component>
  );
});

Card.displayName = 'Card';

export { Card };