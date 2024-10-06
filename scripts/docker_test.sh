#!/bin/sh

set -eou pipefail

apk add gcc musl-dev libffi-dev openssl-dev python3-dev cargo
pip install tox poetry
tox -e py-mypy
