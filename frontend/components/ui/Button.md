# Button Component Documentation

The Button component is a professional, responsive button implementation for the todo app built with Next.js and Tailwind CSS.

## Features

- **Multiple Variants**: Primary, secondary, and destructive variants
- **Different Sizes**: Small, medium, and large sizes
- **Loading State**: Visual loading indicator with spinner
- **Accessibility**: Proper ARIA attributes and keyboard navigation
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **TypeScript Support**: Full type safety with detailed interfaces

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'destructive'` | `'primary'` | Visual style of the button |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Size of the button |
| `isLoading` | `boolean` | `false` | Shows loading spinner and disables button |
| `children` | `ReactNode` | - | Content inside the button |
| `className` | `string` | `''` | Additional CSS classes |
| `disabled` | `boolean` | `false` | Disables the button |

## Usage Examples

```tsx
import Button from '@/components/ui/Button';

// Primary button (default)
<Button>Submit</Button>

// Secondary button
<Button variant="secondary">Cancel</Button>

// Destructive button
<Button variant="destructive">Delete</Button>

// Small button
<Button size="sm">Small</Button>

// Large button
<Button size="lg">Large</Button>

// Loading state
<Button isLoading={true}>Loading...</Button>

// Disabled button
<Button disabled>Disabled</Button>

// With click handler
<Button onClick={() => console.log('Clicked!')}>Click me</Button>
```

## Accessibility

- Proper ARIA attributes for disabled state
- Focus ring for keyboard navigation
- Semantic button element
- Proper color contrast for accessibility

## Styling

- Uses Tailwind CSS utility classes
- Responsive design with mobile-first approach
- Dark mode support
- Smooth transitions and hover effects