FROM nginx:stable-alpine-slim

# Install dependencies
RUN apk add --no-cache netbird curl ca-certificates certbot && rm -rf /var/cache/apk/*

# Add the risenet root cert
COPY risenet_ca.crt /usr/local/share/ca-certificates/risenet_ca.crt
RUN update-ca-certificates

RUN mkdir -p /var/www/certbot

COPY entrypoint.sh entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
