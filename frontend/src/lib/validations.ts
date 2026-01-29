/**
 * Validation schemas using Zod
 * Used with react-hook-form for type-safe form validation
 *
 * Phase V: Extended with priority and due_date validation
 */

import { z } from 'zod';

/**
 * Task form validation schema
 * Phase V: Extended with priority, due_date, and tags fields
 */
export const taskFormSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim(),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .trim()
    .optional()
    .or(z.literal('')),

  // Phase V: Priority (US1)
  priority: z.enum(['high', 'medium', 'low']).optional(),

  // Phase V: Due Date (US2)
  due_date: z.string().nullable().optional(),

  // Phase V: Tags (US3)
  tag_ids: z.array(z.number()).optional(),

  // Phase V: Recurring (US7)
  is_recurring: z.boolean().optional(),
  recurring_frequency: z.enum(['daily', 'weekly', 'monthly']).nullable().optional(),

  // Phase V: Reminder (US8)
  reminder_minutes_before: z.number().positive().nullable().optional(),
});

/**
 * Infer TypeScript type from schema
 */
export type TaskFormData = z.infer<typeof taskFormSchema>;

/**
 * Auth validation schemas
 */
export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

export const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
