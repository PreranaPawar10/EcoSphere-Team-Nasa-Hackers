FROM node:20-alpine

WORKDIR /app/ecosphere

COPY app/ecosphere/package*.json ./
RUN apk add --no-cache python3 make g++ gcc
RUN npm install

COPY app/ecosphere/ ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]