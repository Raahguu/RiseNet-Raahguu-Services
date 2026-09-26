FROM nginx:stable-alpine-slim

# Install risenet
RUN apk update && apk add netbird netbird-openrc

CMD ["sh", "-c", "netbird up --management-url https://vpn.lab.st4rburn.dev --disable-firewall && nginx --with-stream_ssl_preread_module -g daemon off;"]
