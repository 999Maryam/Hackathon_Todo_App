# Data Model: Authentication & Security for Todo Full-Stack Web Application

## Overview
This document defines the data structures and relationships for the authentication and security implementation. These models ensure proper user isolation and secure token handling.

## User Entity
**Description**: Represents an authenticated user of the system with unique identifier extracted from JWT token

**Fields**:
- `id` (UUID/String): Unique identifier for the user, matches the user_id in JWT tokens
- `email` (String): User's email address for identification
- `hashed_password` (String): BCrypt hashed password for authentication
- `created_at` (DateTime): Timestamp of account creation
- `updated_at` (DateTime): Timestamp of last account update
- `is_active` (Boolean): Whether the account is active (default: true)

**Validation**:
- Email must be valid format
- Password must meet minimum strength requirements
- User ID must match JWT payload format

**Relationships**:
- One-to-Many: User has many Tasks (foreign key: user_id in Task model)

## Task Entity
**Description**: Personal task entity that belongs to a specific user, with access restricted to the owning user only

**Fields**:
- `id` (UUID/String): Unique identifier for the task
- `title` (String): Task title (required, max 255 chars)
- `description` (Text): Optional task description
- `completed` (Boolean): Whether the task is completed (default: false)
- `user_id` (UUID/String): Foreign key linking to the owning user
- `created_at` (DateTime): Timestamp of task creation
- `updated_at` (DateTime): Timestamp of last task update

**Validation**:
- Title is required and not empty
- User_id must reference an existing user
- Users can only access tasks belonging to their own user_id

**Relationships**:
- Many-to-One: Task belongs to one User (foreign key: user_id)

## JWT Token (Conceptual)
**Description**: Authentication token containing user identity information with expiration time, signed with shared secret

**Payload Structure**:
- `sub` (Subject): User ID (matches user.id in User entity)
- `exp` (Expiration): Unix timestamp for token expiry (7 days from issue)
- `iat` (Issued At): Unix timestamp when token was issued
- `jti` (JWT ID): Unique identifier for the token (optional, for revocation)

**Validation**:
- Signature must be valid using BETTER_AUTH_SECRET
- Current time must be before exp
- Sub field must correspond to a valid user

## Session (Client-Side Concept)
**Description**: Client-side session managed by Better Auth that contains user authentication state

**Attributes**:
- `userId`: Matches the user_id in JWT token
- `expiresAt`: Expiration time of the session
- `accessToken`: The JWT token itself
- `refreshToken`: Refresh token (not used in this implementation due to hackathon scope)

**Validation**:
- Session must be active
- Token must not be expired
- User must exist in the database

## Security Constraints
**Ownership Validation**:
- All task queries must filter by user_id
- API endpoints must validate that user_id in JWT matches the resource owner
- Users cannot access, modify, or delete tasks belonging to other users

**Access Control**:
- Unauthenticated requests return 401 Unauthorized
- Authenticated requests with wrong ownership return 403 Forbidden
- Valid requests return appropriate success responses

## Indexes for Performance
- Index on User.email for login performance
- Index on Task.user_id for ownership filtering
- Composite index on Task.user_id and completed for filtered queries