// Simple test to verify Card component syntax
import React from 'react';
import { Card } from './components/ui/Card';

const TestComponent = () => {
  return (
    <Card
      header={<h2>Test Header</h2>}
      footer={<button>Test Button</button>}
      variant="elevated"
      className="test-class"
    >
      <p>Test content</p>
    </Card>
  );
};

export default TestComponent;