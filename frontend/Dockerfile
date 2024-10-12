FROM node:18-alpine3.19 AS frontend_builder

ADD .  /drone-ai-frontend
WORKDIR /drone-ai-frontend

ENV NODE_OPTIONS=--openssl-legacy-provider
EXPOSE 3000

CMD ["yarn", "start"]
