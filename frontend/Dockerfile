FROM node:18-alpine3.19

ADD .  /drone-ai-frontend
WORKDIR /drone-ai-frontend

RUN yarn install
RUN yarn add dotenv

ENV NODE_OPTIONS=--openssl-legacy-provider
ENV HOST_BACKEND=drone-ai-backend
ENV PORT_BACKEND=8000
ENV HOST=0.0.0.0

EXPOSE 3000

ENTRYPOINT ["yarn", "start"]
