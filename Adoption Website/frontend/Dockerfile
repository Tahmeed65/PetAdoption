FROM node:16-alpine
WORKDIR /main
COPY package*.json ./
RUN npm install
RUN npm install axios js-cookie react-router-dom react-bootstrap bootstrap
COPY . .
CMD ["npm", "run", "dev"]
