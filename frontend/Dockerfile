FROM node:lts-alpine3.16 as builder

ARG VITE_BACKEND_URL
ARG VITE_GOOGLE_ANALYTICS_ID=""
ARG VITE_ADMIN_EMAIL="admin@example.com"

WORKDIR /app

COPY . .

RUN yarn install --immutable && \
    export VITE_BACKEND_URL=$VITE_BACKEND_URL && \
    export VITE_GOOGLE_ANALYTICS_ID=$VITE_GOOGLE_ANALYTICS_ID && \
    export VITE_ADMIN_EMAIL=$VITE_ADMIN_EMAIL && \
    yarn build

FROM nginx:1.21.6-alpine

COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
