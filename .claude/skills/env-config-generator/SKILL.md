# SKILL: env-config-generator

## 1. Purpose
Manage environment variables with type-safe configuration loaders and validation.

## 2. Input Parameters
- `Variables`: List of required keys and descriptions.
- `LoaderType`: Pydantic (Python) or Zod (TS).

## 3. Code Template

### Backend Settings (Pydantic)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### Frontend Config (Zod)
```typescript
import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse({
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
});
```

## 4. Output
`.env.example` file and a configuration loader script.

## 5. Usage Example
Input: `Variables=["DATABASE_URL", "STRIPE_KEY"]`
Output: A settings module that crashes at startup if configured variables are missing.

## 6. Quality Standards
- Always provide `.env.example` with descriptions.
- Fail fast on missing/invalid configuration.
- Use explicit types (int, float, url).
