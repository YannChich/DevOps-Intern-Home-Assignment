# Use Ubuntu as base image as required
FROM ubuntu:22.04

# Install Nginx (and keep image relatively small)
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy our custom Nginx configuration into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the two ports used by our servers
EXPOSE 8080 8081

# Run Nginx in the foreground (required in Docker)
CMD ["nginx", "-g", "daemon off;"]

