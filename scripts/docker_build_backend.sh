#!/bin/bash

set -eou pipefail

docker build -t "${PROJECT}:backend" .
