#!/bin/bash

set -eou pipefail

docker build --build-arg VITE_BACKEND_URL="${VITE_BACKEND_URL}" -t "${PROJECT}:frontend" ./frontend
