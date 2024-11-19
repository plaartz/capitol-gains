FROM node:18-alpine 

WORKDIR /web

COPY package.json .

RUN npm install

RUN npm install react-slider

COPY . .

EXPOSE 5173

CMD [ "npm", "run", "dev" ]