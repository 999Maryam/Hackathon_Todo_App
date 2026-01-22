# Task: T006 | Spec: 008-docker-containerization
# ========================================
# Optimized Multi-Stage Dockerfile
# Next.js Frontend Application
# ========================================

ARG NODE_VERSION=20-alpine
FROM node:${NODE_VERSION} AS base

WORKDIR /app

# ========================================
# Stage 1: Dependencies
# ========================================
FROM base AS deps

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies with cache optimization
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev && \
    npm cache clean --force

# ========================================
# Stage 2: Builder
# ========================================
FROM base AS builder

WORKDIR /app

# Build argument for API URL (used at build time by Next.js)
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Copy package files
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies)
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy node_modules from deps stage (production dependencies)
# Note: We still need to run npm ci above to get devDependencies for build
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build the application
# Next.js will create .next/standalone output (configured in next.config.ts)
RUN npm run build

# ========================================
# Stage 3: Production Runner
# ========================================
FROM base AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Copy standalone output from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./

# Copy static files to correct location
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy public directory for static assets
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Switch to non-root user
USER nextjs

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]
