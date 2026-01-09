# Modal Component

A professional, responsive modal component for the todo app built with Next.js App Router and Tailwind CSS.

## Features

- ✅ Backdrop click to close
- ✅ ESC key to close
- ✅ Header, body, and footer sections
- ✅ Accessible with proper ARIA attributes and focus management
- ✅ TypeScript typing
- ✅ Responsive design with Tailwind CSS
- ✅ Multiple size options (sm, md, lg)

## Usage

```tsx
import Modal from '@/components/ui/Modal';
import Button from '@/components/ui/Button';

const MyComponent = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open Modal</Button>

      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        size="md"
        header={<h2>Modal Title</h2>}
        footer={
          <div className="flex space-x-3">
            <Button variant="secondary" onClick={() => setIsOpen(false)}>Cancel</Button>
            <Button variant="primary">Save</Button>
          </div>
        }
      >
        <p>Modal content goes here</p>
      </Modal>
    </>
  );
};
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| isOpen | boolean | required | Controls whether the modal is open or closed |
| onClose | () => void | required | Function to call when modal should be closed |
| children | React.ReactNode | required | Content to display in the modal body |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Size of the modal |
| header | React.ReactNode | undefined | Content to display in the modal header |
| footer | React.ReactNode | undefined | Content to display in the modal footer |
| className | string | '' | Additional CSS classes to apply to the modal |

## Accessibility Features

- Proper ARIA attributes (`aria-modal="true"`, `role="dialog"`)
- Focus management (focus trapped within modal)
- ESC key support
- Backdrop click to close
- Screen reader friendly
- Keyboard navigation support