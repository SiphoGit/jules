# ---- Base Node image for both build and run stages ----
# Using Alpine for a smaller image size
FROM node:18-alpine AS base

# Set environment variables
ENV NODE_ENV=production

# ---- Builder Stage ----
# Responsible for building the Next.js application
FROM base AS builder

WORKDIR /app

# Copy package.json and lock file
# Assuming npm, adjust if yarn is used (e.g., copy yarn.lock and use yarn install)
COPY package.json package-lock.json* ./
# If yarn.lock exists and package-lock.json does not, you might need:
# COPY package.json yarn.lock ./

# Install all dependencies (including devDependencies needed for build)
RUN npm install
# If using yarn:
# RUN yarn install

# Copy the rest of the application source code
COPY . .

# Build the Next.js application
# This will generate the .next folder
RUN npm run build
# If using yarn:
# RUN yarn build


# ---- Runner Stage ----
# Responsible for running the built Next.js application
FROM base AS runner

WORKDIR /app

# Copy necessary files from the builder stage
# Copy .next folder (contains the built app)
COPY --from=builder /app/.next ./.next
# Copy public folder
COPY --from=builder /app/public ./public
# Copy next.config.js (needed to run the app)
COPY next.config.js .
# Copy package.json to install production dependencies
COPY package.json .
# If you have a server.js for custom server, copy that too. Assuming default Next.js start.

# Install production dependencies only
# npm ci --omit=dev might be better if package-lock.json is strictly followed
RUN npm install --omit=dev
# If using yarn:
# RUN yarn install --production

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
# This will use the start script defined in package.json (usually "next start")
CMD ["npm", "start"]
# If using yarn:
# CMD ["yarn", "start"]
