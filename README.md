# DevOps Intern – Home Assignment (F5)
## Advanced Features Branch

This branch (`advanced-features`) contains an extended version of the project implementing
the optional advanced requirements described in the assignment. The goal of this branch is
to demonstrate additional Nginx features, experimentation, and engineering reasoning beyond
the baseline solution available in the `main` branch.

---

## Project Overview

In addition to the base implementation, this branch introduces:

- HTTPS support using a self-signed TLS certificate
- Rate limiting configuration in Nginx (5 requests per second per client IP)
- An extended test suite attempting to validate rate limiting behavior
- Documentation of design choices, trade-offs, and limitations encountered

The `main` branch remains the stable reference implementation for the mandatory requirements.

---

## Architecture

The architecture remains identical to the main branch:

- An **Nginx container** exposing multiple HTTP endpoints
- A **Python test container** validating server behavior
- **Docker Compose** used to orchestrate and network the services
- **GitHub Actions CI** relying on the test container exit code

Only the Nginx configuration and tests were extended in this branch.

---

## HTTPS Support

HTTPS support was added to the Nginx container using a self-signed certificate.

### Implementation details

- OpenSSL is installed in the Nginx image at build time
- A self-signed RSA certificate is generated during the image build
- An HTTPS server block listens on port **8443**
- The certificate and private key are stored under `/etc/nginx/ssl`

This setup is intended for demonstration and testing purposes only and is not suitable for
production use.

---

## Rate Limiting

### Configuration

Rate limiting is implemented using Nginx’s `limit_req_zone` and `limit_req` directives:

```nginx
limit_req_zone $binary_remote_addr zone=perip:10m rate=5r/s;
limit_req_status 429;
```

This configuration limits each client IP to **5 requests per second**.

The rate limit is applied to the main HTTP success endpoint on port 8080:

```nginx
location / {
    limit_req zone=perip burst=1 nodelay;
    ...
}
```

When the limit is exceeded, Nginx returns HTTP status **429 (Too Many Requests)**.

---

## Rate Limiting Validation – Tests and Limitations

### Test approach

The Python test suite was extended to attempt validation of the rate limiting behavior by:

- Sending a very large number of HTTP requests
- Using a high number of concurrent threads
- Expecting at least one request to be rejected with HTTP 429

This approach aims to simulate a burst of traffic from a single client IP.

### Observed behavior

Despite increasing concurrency (hundreds of threads) and total request count (up to thousands
of requests), the test was **not able to reliably trigger HTTP 429 responses** while keeping
the rate limit configured at **5 requests per second**.

### Analysis

This behavior is due to several factors:

- Nginx’s internal rate limiting algorithm (token bucket–based) smooths request handling
- Network, HTTP, and Docker-related latency reduce the effective request rate
- Requests are not guaranteed to fall within the same one-second time window, even when sent
  concurrently from the test container

As a result, the observed effective throughput remains below the configured threshold.

### Conclusion

The rate limiting configuration is correct and active, but validating a **5r/s limit in a
deterministic way inside an automated CI environment** proved unreliable without modifying
the rate threshold or introducing a dedicated test endpoint.

This limitation and the attempted mitigation strategies are intentionally documented to
demonstrate the investigation and reasoning process.

---

## Changing the Rate Limit Threshold

The rate limit can be adjusted by modifying the `rate` parameter in the Nginx configuration:

```nginx
limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;
```

After changing the value, the Nginx container must be rebuilt and restarted:

```bash
docker compose up --build
```

---

## Docker Compose

Docker Compose usage is unchanged from the main branch and is used to:

- Build the Nginx and test images
- Run both containers on the same Docker network
- Allow the test container to access Nginx by service name

To run locally:

```bash
docker compose up --build
```

---

## Project Structure

```
.
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── tests/
│   ├── Dockerfile
│   └── test_app.py
├── Resource/screenshots/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
└── README.md
```

---

## Engineering Notes

- The `main` branch should be considered the stable reference solution
- This branch focuses on experimentation and optional features
- Limitations encountered during testing are explicitly documented rather than hidden
- The intent is to show practical understanding, debugging, and trade-off analysis

---

## Author

DevOps Intern Candidate  
Computer Science Student

