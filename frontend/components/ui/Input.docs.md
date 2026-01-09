# Input Component Documentation

The Input component is a versatile, accessible, and responsive input field component built with React, TypeScript, and Tailwind CSS.

## Features

- Supports multiple input types (text, email, password, number, tel, url, search, date, time, datetime-local)
- Accessible with proper ARIA attributes
- Error state with error message display
- Disabled state
- Responsive design
- TypeScript typing
- Customizable styling with Tailwind classes
- Proper label and placeholder support

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `'text' \| 'email' \| 'password' \| 'number' \| 'tel' \| 'url' \| 'search' \| 'date' \| 'time' \| 'datetime-local'` | `'text'` | Type of input element |
| `label` | `string` | `undefined` | Label for the input field |
| `placeholder` | `string` | `undefined` | Placeholder text for the input field |
| `error` | `string` | `undefined` | Error message to display when input is invalid |
| `disabled` | `boolean` | `false` | Whether the input field is disabled |
| `className` | `string` | `''` | Additional CSS classes to apply |
| `id` | `string` | required | ID for the input field (required for accessibility) |
| `required` | `boolean` | `false` | Whether the input field is required |
| ...rest | `InputHTMLAttributes<HTMLInputElement>` | - | All other standard input attributes |

## Usage Examples

### Basic Text Input
```tsx
<Input
  id="name-input"
  label="Name"
  placeholder="Enter your name"
/>
```

### Email Input with Validation
```tsx
<Input
  id="email-input"
  label="Email"
  type="email"
  placeholder="Enter your email"
  error={emailError}
  required
/>
```

### Disabled Input
```tsx
<Input
  id="disabled-input"
  label="Disabled Field"
  placeholder="This field is disabled"
  disabled={true}
/>
```

### Password Input
```tsx
<Input
  id="password-input"
  label="Password"
  type="password"
  placeholder="Enter your password"
  required
/>
```

## Accessibility Features

- Proper `id`/`htmlFor` association between label and input
- `aria-invalid` and `aria-describedby` attributes for error states
- `role="alert"` for error messages
- `aria-live="polite"` for dynamic error messages
- Proper focus management with visible focus rings
- Required field indicators

## Styling

The component uses Tailwind CSS for styling with:

- Responsive design that works on all screen sizes
- Focus states with blue ring
- Error states with red border
- Disabled states with reduced opacity
- Dark mode support
- Smooth transitions

## Testing

The component includes comprehensive tests covering:

- Basic rendering
- Different input types
- Error states
- Disabled states
- ARIA attributes
- Event handling
- Accessibility features
- Ref forwarding