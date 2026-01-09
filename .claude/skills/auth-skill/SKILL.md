---
name: auth-skill
description: Implement secure authentication including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Accept email/username and password
   - Validate input (length, format, required fields)
   - Hash password before storage
   - Prevent duplicate accounts

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords securely
   - Handle invalid credentials gracefully
   - Return authentication tokens on success

3. **Password Hashing**
   - Use industry-standard hashing algorithms (bcrypt or argon2)
   - Apply proper salt rounds
   - Never store plaintext passwords
   - Support password updates and resets

4. **JWT Token Handling**
   - Generate access tokens on successful signin
   - Include user identifier and expiry in payload
   - Verify tokens for protected routes
   - Support token expiration and refresh logic

5. **Better Auth Integration**
   - Integrate Better Auth for session management
   - Configure providers and secrets securely
   - Support middleware-based route protection
   - Ensure compatibility with modern frameworks (Next.js / API routes)

## Best Practices
- Always hash passwords before persisting
- Use HTTPS for all auth-related requests
- Keep JWT secrets in environment variables
- Set short-lived access tokens
- Separate authentication and authorization logic
- Log authentication events without sensitive data
- Follow OWASP authentication guidelines

## Example Structure
```ts
// Signup
POST /api/auth/signup
{
  email: string,
  password: string
}

// Signin
POST /api/auth/signin
{
  email: string,
  password: string
}

// Protected Route
GET /api/user/profile
Authorization: Bearer <JWT_TOKEN>
