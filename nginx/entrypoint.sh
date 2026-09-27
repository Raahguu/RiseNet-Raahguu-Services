#!/bin/sh

netbird service run &

# Wait until the service is up
until [ -S /var/run/netbird.sock ]; do
    sleep 0.2
done

# Should output 'already connected' if this is not the first time running
netbird up --management-url https://vpn.lab.st4rburn.dev --disable-firewall

# Get HTTPS Working
CERT="/etc/letsencrypt/live/"
if [ -z $(ls -A "$CERT") ]; then
    echo "Setting up Cert issuing"
    echo "Starting HTTP-only nginx server"

    # 1. Start HTTP-Only server
    nginx -c /etc/nginx/http-only.conf

    sleep 30s

    # 2. Get the certs
    certbot certonly --webroot -w /var/www/certbot \
            --redirect -n --keep --expand --agree-tos \
            --server https://ca.risenet/acme/acme/directory \
            -d blockchain.rise -d raahguu.nya -d lounge.uwu \
            -m raahguu@dotmail.rise
    
    # 3. Certs exist, turn off nginx
    nginx -s quit
else
    echo "$CERT contains:"
    ls -A "$CERT"
    echo "EOL"
fi

# Setup CERT Renewal
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); echo "0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q --post-hook nginx -s reload" | tee -a /etc/crontab > /dev/null

# Start normal nginx
exec nginx -g 'daemon off;'
