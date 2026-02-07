# Use Ubuntu as base image as required
FROM ubuntu:22.04

# Install Nginx and OpenSSL (for self-signed certificate)
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx openssl \
    && rm -rf /var/lib/apt/lists/*

# Generate a self-signed certificate for HTTPS
# The certificate is valid for 365 days and uses CN=localhost
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout /etc/nginx/ssl/selfsigned.key \
      -out /etc/nginx/ssl/selfsigned.crt \
      -subj "/CN=localhost"

# Copy our custom Nginx configuration into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the HTTP/HTTPS ports
EXPOSE 8080 8081 8443

# Run Nginx in the foreground (required in Docker)
CMD ["nginx", "-g", "daemon off;"]

