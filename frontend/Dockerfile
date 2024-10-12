FROM node:18-alpine3.19

ADD .  /drone-ai-frontend
WORKDIR /drone-ai-frontend

ENV NODE_OPTIONS=--openssl-legacy-provider
ENV HOST=drone-ai-backend

RUN yarn install

EXPOSE 3000

ENTRYPOINT ["yarn", "start"]
