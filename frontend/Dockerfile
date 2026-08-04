# Frontend multi-stage Dockerfile: build with Node then serve with nginx

# Build stage
FROM node:18-alpine AS build
WORKDIR /build
COPY package.json package-lock.json* ./
COPY tsconfig.json vite.config.ts ./
COPY src ./src
COPY index.html ./
RUN npm ci --silent
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=build /build/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
