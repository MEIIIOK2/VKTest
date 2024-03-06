FROM node:16-alpine

WORKDIR /frontend

COPY ./package*.json /frontend

RUN npm install

COPY . /frontend

CMD [ "npm","run","build" ]