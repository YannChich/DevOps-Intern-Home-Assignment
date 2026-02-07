import sys
import time
import urllib.request
import urllib.error
import os

# Basic configuration for the tests
TARGET_HOST = os.getenv("TARGET_HOST", "nginx")  # Hostname of the Nginx service in Docker network
PORT_SUCCESS = 8080
PORT_ERROR = 8081
EXPECTED_TEXT = "Welcome from Nginx on port 8080"

MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 2


def http_get(url: str):
    """
    Perform a simple HTTP GET request and return (status_code, body_as_str).
    If the request fails, an exception is raised.
    """
    try:
        with urllib.request.urlopen(url) as response:
            status_code = response.getcode()
            body = response.read().decode("utf-8", errors="ignore")
            return status_code, body
    except urllib.error.HTTPError as e:
        # HTTPError is raised for non-2xx responses; we still want the status code
        body = e.read().decode("utf-8", errors="ignore")
        return e.code, body
    except urllib.error.URLError as e:
        # URLError typically means connection issues (e.g., service not ready)
        raise RuntimeError(f"Failed to connect to {url}: {e}")


def wait_for_service(host: str, port: int) -> None:
    """
    Wait for the HTTP service to become reachable.
    This helps when the test container starts before Nginx is fully ready.
    """
    url = f"http://{host}:{port}/"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            status_code, _ = http_get(url)
            # If we get any HTTP response, we consider the service "up"
            print(f"[INFO] Service at {url} is up (received status {status_code})")
            return
        except RuntimeError as e:
            print(f"[INFO] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            time.sleep(RETRY_DELAY_SECONDS)
    raise RuntimeError(f"Service at {url} did not become ready after {MAX_RETRIES} attempts")


def test_success_server() -> bool:
    """
    Test the 'success' Nginx server:
    - Must return HTTP 200
    - Body must contain a specific text
    """
    url = f"http://{TARGET_HOST}:{PORT_SUCCESS}/"
    print(f"[TEST] Checking success server at {url}")
    status_code, body = http_get(url)

    if status_code != 200:
        print(f"[ERROR] Expected status 200 but got {status_code}")
        return False

    if EXPECTED_TEXT not in body:
        print(f"[ERROR] Expected text not found in response body")
        return False

    print("[OK] Success server returned 200 and expected content")
    return True


def test_error_server() -> bool:
    """
    Test the 'error' Nginx server:
    - Must return an HTTP error code (here we expect 500)
    """
    url = f"http://{TARGET_HOST}:{PORT_ERROR}/"
    print(f"[TEST] Checking error server at {url}")
    status_code, _ = http_get(url)

    if status_code != 500:
        print(f"[ERROR] Expected status 500 but got {status_code}")
        return False

    print("[OK] Error server returned expected status 500")
    return True


def main() -> int:
    """
    Entry point for the test script.
    Returns 0 if all tests pass, non-zero otherwise.
    """
    try:
        # Ensure the main service is reachable before running tests
        wait_for_service(TARGET_HOST, PORT_SUCCESS)
    except RuntimeError as e:
        print(f"[FATAL] {e}")
        return 1

    all_ok = True

    if not test_success_server():
        all_ok = False

    if not test_error_server():
        all_ok = False

    if all_ok:
        print("[RESULT] All tests passed ✅")
        return 0
    else:
        print("[RESULT] Some tests failed ❌")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

