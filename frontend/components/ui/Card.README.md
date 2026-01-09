# Card Component

A responsive, accessible Card component for the todo app built with Next.js and Tailwind CSS.

## Features

- Header, body, and footer sections
- Multiple variants (default, elevated)
- Custom styling support via className prop
- Fully accessible with proper semantic HTML
- TypeScript typing
- Responsive design with Tailwind CSS
- Forward ref support

## Usage

```tsx
import { Card } from '@/components/ui/Card';

// Basic card with all sections
<Card
  header={<h3>Card Title</h3>}
  footer={<button>Action</button>}
>
  <p>Card content goes here</p>
</Card>

// Minimal card with just body content
<Card>
  <p>Just body content</p>
</Card>

// Elevated card variant
<Card variant="elevated" header={<h3>Important Card</h3>}>
  <p>This card stands out more</p>
</Card>

// Card with custom styling
<Card className="border-blue-300 bg-blue-50">
  <p>Custom styled card</p>
</Card>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| header | React.ReactNode | undefined | Content for the card header section |
| children | React.ReactNode | undefined | Main content of the card (body) |
| footer | React.ReactNode | undefined | Content for the card footer section |
| variant | 'default' \| 'elevated' | 'default' | Visual variant of the card |
| className | string | '' | Additional CSS classes to apply |
| as | React.ElementType | 'div' | HTML element to render as the card container |
| role | string | 'region' | Accessibility role for the card |
| aria-label | string | undefined | ARIA label for accessibility |
| aria-labelledby | string | undefined | ARIA labelledby for accessibility |

## Styling

The Card component uses Tailwind CSS utility classes and supports:

- Responsive design that works on all screen sizes
- Dark mode styling
- Smooth transitions for interactive states
- Proper spacing and padding
- Border and shadow variations based on variant