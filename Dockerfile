FROM node:18-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Instalar dependencias
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# Copiar aplicación
COPY . .

# Exponer puerto
EXPOSE 3000

# Comando por defecto
CMD ["npm", "run", "dev"]