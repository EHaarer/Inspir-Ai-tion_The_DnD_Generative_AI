FROM node:20-alpine 
WORKDIR /app
COPY package-lock.json .
COPY package.json .
EXPOSE 3000
COPY . .
RUN npm install
CMD npm run dev
