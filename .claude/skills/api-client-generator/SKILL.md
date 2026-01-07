# SKILL: api-client-generator

## 1. Purpose
Generate a type-safe, production-grade API client for interacting with the backend, featuring JWT handling, CRUD methods, and robust error parsing.

## 2. Input Parameters
- `BaseUrl`: Root API URL.
- `ResourceName`: Name of the entity (e.g., Task).
- `Endpoints`: List of CRUD operations needed.

## 3. Code Template

```typescript
import { apiFetch } from './apiFetch'; // Utility that handles base URL and headers

export interface {{ResourceName}} {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  owner_id: number;
  created_at: string;
}

export type {{ResourceName}}Create = Pick<{{ResourceName}}, 'title' | 'description'>;
export type {{ResourceName}}Update = Partial<{{ResourceName}}Create> & { is_completed?: boolean };

export class {{ResourceName}}Client {
  private static readonly PATH = '/api/{{ResourceName | lower}}s';

  static async list(params?: { skip?: number; limit?: number }): Promise<{{ResourceName}}[]> {
    const searchParams = new URLSearchParams(params as any).toString();
    const response = await apiFetch(`${this.PATH}/?${searchParams}`);
    return response.json();
  }

  static async get(id: number): Promise<{{ResourceName}}> {
    const response = await apiFetch(`${this.PATH}/${id}`);
    return response.json();
  }

  static async create(data: {{ResourceName}}Create): Promise<{{ResourceName}}> {
    const response = await apiFetch(this.PATH, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return response.json();
  }

  static async update(id: number, data: {{ResourceName}}Update): Promise<{{ResourceName}}> {
    const response = await apiFetch(`${this.PATH}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    return response.json();
  }

  static async delete(id: number): Promise<void> {
    await apiFetch(`${this.PATH}/${id}`, {
      method: 'DELETE',
    });
  }
}
```

## 4. Output
A TypeScript file with an exported Client class containing static methods for API interaction and matching type interfaces.

## 5. Usage Example
Input: `ResourceName="Project"`
Output: A `ProjectClient` class providing `list()`, `get()`, `create()`, etc., with full TypeScript Intellisense for request and response payloads.

## 6. Quality Standards
- Strong typing for all request/response objects.
- Centralized `apiFetch` utility for consistent auth header (JWT) and base URL handling.
- Clear separation between DB models and API-facing types (Create/Update).
- Return promises with proper error propagation.
