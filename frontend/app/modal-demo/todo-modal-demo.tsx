'use client';

import React, { useState } from 'react';
import Modal from '@/components/ui/Modal';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
}

const TodoModalDemo = () => {
  const [todos, setTodos] = useState<Todo[]>([
    { id: '1', title: 'Sample Todo', description: 'This is a sample todo item', completed: false },
    { id: '2', title: 'Another Task', description: 'Another example task', completed: true },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTodo, setCurrentTodo] = useState<Todo | null>(null);
  const [formState, setFormState] = useState({ title: '', description: '' });

  const openEditModal = (todo: Todo) => {
    setCurrentTodo(todo);
    setFormState({ title: todo.title, description: todo.description });
    setIsModalOpen(true);
  };

  const openAddModal = () => {
    setCurrentTodo(null);
    setFormState({ title: '', description: '' });
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentTodo(null);
  };

  const handleSave = () => {
    if (currentTodo) {
      // Update existing todo
      setTodos(todos.map(todo =>
        todo.id === currentTodo.id
          ? { ...todo, title: formState.title, description: formState.description }
          : todo
      ));
    } else {
      // Add new todo
      const newTodo: Todo = {
        id: Date.now().toString(),
        title: formState.title,
        description: formState.description,
        completed: false,
      };
      setTodos([...todos, newTodo]);
    }
    closeModal();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormState(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">Todo App with Modal</h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Your Todos</h2>
            <Button onClick={openAddModal} variant="primary">
              Add Todo
            </Button>
          </div>

          <div className="space-y-4">
            {todos.map(todo => (
              <div
                key={todo.id}
                className={`p-4 rounded-md border ${
                  todo.completed
                    ? 'bg-green-50 border-green-200'
                    : 'bg-white border-gray-200'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {todo.title}
                    </h3>
                    <p className="text-gray-600 mt-1">{todo.description}</p>
                  </div>
                  <Button
                    variant={todo.completed ? 'secondary' : 'primary'}
                    size="sm"
                    onClick={() => openEditModal(todo)}
                  >
                    {todo.completed ? 'Completed' : 'Edit'}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Modal Component */}
        <Modal
          isOpen={isModalOpen}
          onClose={closeModal}
          size="md"
          header={
            <div className="flex items-center">
              <h3 className="text-lg font-semibold text-gray-900">
                {currentTodo ? 'Edit Todo' : 'Add New Todo'}
              </h3>
            </div>
          }
          footer={
            <div className="flex space-x-3">
              <Button
                variant="secondary"
                onClick={closeModal}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleSave}
              >
                Save
              </Button>
            </div>
          }
        >
          <div className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <Input
                id="title"
                name="title"
                value={formState.title}
                onChange={handleInputChange}
                placeholder="Enter todo title"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <Input
                id="description"
                name="description"
                value={formState.description}
                onChange={handleInputChange}
                placeholder="Enter todo description"
              />
            </div>

            {currentTodo && (
              <div className="pt-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={currentTodo.completed}
                    onChange={() => {}}
                    className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  />
                  <span className="ml-2 text-sm text-gray-700">Mark as completed</span>
                </label>
              </div>
            )}
          </div>
        </Modal>
      </div>
    </div>
  );
};

export default TodoModalDemo;