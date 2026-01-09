---
name: backend-api-generator
description: Generate backend API routes, handle requests and responses, and connect to a database. Use for building scalable backend services.
---

# Backend API Development

## Instructions

1. **Route generation**
   - RESTful route structure
   - Versioned API paths
   - Clear resource naming

2. **Request & response handling**
   - Validate request payloads
   - Standardized success/error responses
   - Proper HTTP status codes

3. **Database integration**
   - Establish DB connection
   - Perform CRUD operations
   - Handle connection errors safely

4. **Middleware usage**
   - Authentication & authorization
   - Logging and error handling
   - Request parsing (JSON, params)

## Best Practices
- Keep controllers thin and focused
- Use service or repository layers
- Never expose raw DB errors
- Follow consistent response schemas
- Environment-based configuration

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { createUser, getUsers } from "../controllers/user.controller.js";

const router = express.Router();

router.post("/", createUser);
router.get("/", getUsers);

export default router;
