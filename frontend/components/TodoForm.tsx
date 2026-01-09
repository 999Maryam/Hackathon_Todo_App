import React, { useState } from 'react';
import Input from '@/components/ui/Input';

interface TodoFormProps {
  onAddTodo: (text: string) => void;
}

const TodoForm: React.FC<TodoFormProps> = ({ onAddTodo }) => {
  const [todoText, setTodoText] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!todoText.trim()) {
      setError('Todo text is required');
      return;
    }

    onAddTodo(todoText);
    setTodoText('');
    setError('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <Input
        id="todo-input"
        label="Add New Todo"
        placeholder="What needs to be done?"
        value={todoText}
        onChange={(e) => {
          setTodoText(e.target.value);
          if (error) setError(''); // Clear error when user starts typing
        }}
        error={error}
        required
      />
      <button
        type="submit"
        className="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md"
      >
        Add Todo
      </button>
    </form>
  );
};

export default TodoForm;