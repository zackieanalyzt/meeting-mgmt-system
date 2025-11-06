FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=development

# Install system dependencies
RUN apk add --no-cache \
    git \
    curl

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production=false \
    && npm cache clean --force

# Create non-root user
RUN addgroup -g 1001 -S nodejs \
    && adduser -S nextjs -u 1001

# Copy project files
COPY . .

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5173/ || exit 1

# Default command (can be overridden in docker-compose)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]