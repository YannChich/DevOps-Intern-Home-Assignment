# Use a small Python base image to keep the test image lightweight
FROM python:3.12-alpine

# Set working directory inside the container
WORKDIR /app

# Copy the test script into the container
COPY test_app.py /app/test_app.py

# Create a non-root user to run the tests (security best practice)
RUN addgroup -S app && adduser -S app -G app

# Switch to the non-root user
USER app

# Default command: run the test script
CMD ["python", "test_app.py"]

