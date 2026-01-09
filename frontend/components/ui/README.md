# UI Components

This directory contains reusable UI components for the todo app.

## Available Components

### Button

A professional, responsive Button component with the following features:

- Multiple variants: primary, secondary, destructive
- Different sizes: sm, md, lg
- Loading state with spinner animation
- Accessibility support with proper ARIA attributes
- TypeScript typing
- Responsive design with Tailwind CSS
- Dark mode support

#### Usage

```tsx
import Button from '@/components/ui/Button';

// Basic usage
<Button>Click me</Button>

// With variant
<Button variant="secondary">Secondary</Button>

// With size
<Button size="lg">Large</Button>

// With loading state
<Button isLoading={true}>Loading...</Button>
```

For more detailed documentation, see [Button.md](./Button.md).

### Input

A versatile, accessible, and responsive input field component with support for various input types, labels, error states, and more.

#### Features

- Supports multiple input types (text, email, password, number, tel, url, search, date, time, datetime-local)
- Accessible with proper ARIA attributes
- Error state with error message display
- Disabled state
- Responsive design
- TypeScript typing
- Customizable styling with Tailwind classes
- Proper label and placeholder support

#### Usage

```tsx
import Input from '@/components/ui/Input';

<Input
  id="email-input"
  label="Email"
  type="email"
  placeholder="Enter your email"
  error={emailError}
  required
/>
```

For more detailed documentation, see [Input.docs.md](./Input.docs.md).