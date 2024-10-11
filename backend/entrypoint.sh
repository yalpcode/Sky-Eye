#!/bin/sh

set -eu

uvicorn --workers "$WORKERS" --host "$HOST" --port "$PORT" "--proxy-headers" "--forwarded-allow-ips" "*" src.main:app
