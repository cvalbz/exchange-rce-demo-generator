#!/usr/bin/env python3
"""Create the Flask demo marker through its command endpoint."""

import argparse
from http.client import HTTPException
import json
import os
import time
from urllib.request import Request, urlopen


def post(base, endpoint, payload, timeout):
    request = Request(
        base + endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-create", action="store_true")
    args = parser.parse_args(argv)
    base = os.environ["TARGET_URL"].rstrip("/")
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        try:
            echoed = post(base, "/echo", {"input": "ready"}, timeout=3)
            if echoed != {"input": "ready"}:
                raise RuntimeError("The echo endpoint returned unexpected data.")
            break
        except (OSError, HTTPException):
            time.sleep(0.5)
    else:
        raise TimeoutError("The Flask application did not become ready.")
    if args.no_create:
        print(json.dumps({"case": "no-create", "expected_oracle_answer": False}))
        return 0
    result = post(base, "/run", {"command": "touch /tmp/rce_achieved"}, timeout=10)
    if result.get("exit_code") != 0:
        raise RuntimeError("The marker creation command failed.")
    print(json.dumps({"case": "create-marker", "exit_code": 0, "expected_oracle_answer": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
