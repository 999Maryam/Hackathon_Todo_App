'use client';

import React, { useState } from 'react';
import Input from '@/components/ui/Input';

const InputDemoPage = () => {
  const [formData, setFormData] = useState({
    text: '',
    email: '',
    password: '',
    number: '',
    tel: '',
    url: '',
    search: '',
    date: '',
    time: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [disabled, setDisabled] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email && !disabled) {
      newErrors.email = 'Email is required';
    } else if (formData.email && !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.password && !disabled) {
      newErrors.password = 'Password is required';
    } else if (formData.password && formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      console.log('Form submitted:', formData);
      alert('Form submitted successfully!');
    }
  };

  const toggleDisabled = () => {
    setDisabled(!disabled);
    if (!disabled) {
      setErrors({});
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-8">Input Component Demo</h1>

      <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-md">
        <p className="text-gray-700 dark:text-gray-300">
          This page demonstrates the Input component with various types and states.
        </p>
      </div>

      <div className="mb-6 flex items-center gap-4">
        <button
          onClick={toggleDisabled}
          className={`px-4 py-2 rounded-md ${
            disabled
              ? 'bg-green-500 hover:bg-green-600 text-white'
              : 'bg-gray-500 hover:bg-gray-600 text-white'
          }`}
        >
          {disabled ? 'Enable Inputs' : 'Disable Inputs'}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input
            id="text-input"
            name="text"
            label="Text Input"
            placeholder="Enter text here"
            value={formData.text}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="email-input"
            name="email"
            label="Email Input"
            placeholder="Enter your email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            disabled={disabled}
            error={errors.email}
            required
          />

          <Input
            id="password-input"
            name="password"
            label="Password Input"
            placeholder="Enter your password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            disabled={disabled}
            error={errors.password}
            required
          />

          <Input
            id="number-input"
            name="number"
            label="Number Input"
            placeholder="Enter a number"
            type="number"
            value={formData.number}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="tel-input"
            name="tel"
            label="Phone Number"
            placeholder="Enter phone number"
            type="tel"
            value={formData.tel}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="url-input"
            name="url"
            label="Website URL"
            placeholder="https://example.com"
            type="url"
            value={formData.url}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="search-input"
            name="search"
            label="Search Input"
            placeholder="Search..."
            type="search"
            value={formData.search}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="date-input"
            name="date"
            label="Date Input"
            type="date"
            value={formData.date}
            onChange={handleChange}
            disabled={disabled}
          />

          <Input
            id="time-input"
            name="time"
            label="Time Input"
            type="time"
            value={formData.time}
            onChange={handleChange}
            disabled={disabled}
          />
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <button
            type="button"
            onClick={() => {
              setFormData({
                text: '',
                email: '',
                password: '',
                number: '',
                tel: '',
                url: '',
                search: '',
                date: '',
                time: '',
              });
              setErrors({});
            }}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-md transition-colors"
          >
            Reset
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputDemoPage;