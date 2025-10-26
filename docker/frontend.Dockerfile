# Frontend service
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm i
COPY frontend ./
# Build and serve with Vite preview for simplicity
RUN npm run build
EXPOSE 5173
ENV VITE_PORT=5173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]

