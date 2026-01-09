---
name: database-schema-builder
description: Design relational database schemas, create tables, and manage migrations. Use for backend and full-stack projects.
---

# Database Schema & Migration Design

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Define primary and foreign keys
   - Normalize data where appropriate

2. **Table creation**
   - Use clear, consistent naming conventions
   - Define data types accurately
   - Add constraints (NOT NULL, UNIQUE, DEFAULT)

3. **Migrations**
   - Create versioned migration files
   - Ensure migrations are reversible
   - Avoid destructive changes without backups

4. **Indexes & performance**
   - Add indexes to frequently queried columns
   - Optimize for read-heavy operations
   - Avoid over-indexing

## Best Practices
- Follow database normalization rules (up to 3NF where possible)
- Use snake_case for table and column names
- Always include timestamps (`created_at`, `updated_at`)
- Keep migrations small and incremental
- Test migrations on staging before production

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migration rollback example
DROP TABLE IF EXISTS users;
