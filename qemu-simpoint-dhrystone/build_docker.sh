#!/bin/bash

set -e

IMAGE_NAME="qemu-simpoint-dhrystone"
docker build -t "$IMAGE_NAME" .
