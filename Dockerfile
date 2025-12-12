FROM python:3.11-slim

WORKDIR /app

# Copiar package files
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Instalar dependencias
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# Copiar aplicación
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
