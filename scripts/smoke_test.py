import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def get_json(url: str, timeout_seconds: int = 10) -> dict | list:
    with urlopen(url, timeout=timeout_seconds) as response:
        status_code = response.getcode()

        if status_code != 200:
            raise RuntimeError(f"Expected HTTP 200 from {url}, got {status_code}")

        body = response.read().decode("utf-8")
        return json.loads(body)


def smoke_test(base_url: str, retries: int, delay_seconds: int) -> int:
    base_url = base_url.rstrip("/")

    health_url = f"{base_url}/health"
    version_url = f"{base_url}/version"
    trades_url = f"{base_url}/trades"

    print(f"Running smoke tests against: {base_url}")

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            print(f"\nAttempt {attempt}/{retries}")

            health = get_json(health_url)
            print(f"/health response: {health}")

            if health.get("status") != "Healthy":
                raise RuntimeError("Health check did not return status Healthy")

            version = get_json(version_url)
            print(f"/version response: {version}")

            if version.get("app") != "cloud-trade-api":
                raise RuntimeError("Version endpoint returned unexpected app name")

            trades = get_json(trades_url)
            print(f"/trades response count: {len(trades)}")

            if not isinstance(trades, list) or len(trades) == 0:
                raise RuntimeError("Trades endpoint did not return trade data")

            print("\n✅ Smoke test passed")
            return 0

        except (HTTPError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as error:
            last_error = error
            print(f"Smoke test attempt failed: {error}")

            if attempt < retries:
                print(f"Waiting {delay_seconds} seconds before retrying...")
                time.sleep(delay_seconds)

    print("\n❌ Smoke test failed")
    print(f"Last error: {last_error}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test deployed Cloud Trade API")
    parser.add_argument("--base-url", required=True, help="Base URL of deployed app")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--delay-seconds", type=int, default=10)

    args = parser.parse_args()

    return smoke_test(
        base_url=args.base_url,
        retries=args.retries,
        delay_seconds=args.delay_seconds,
    )


if __name__ == "__main__":
    sys.exit(main())