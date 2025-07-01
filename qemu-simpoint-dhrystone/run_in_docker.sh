#!/bin/bash

IMAGE_NAME="qemu-simpoint-dhrystone"
OUTPUT_DIR="$(pwd)/simpoint_output"
INTERVAL=100
MAX_K=30

mkdir -p "$OUTPUT_DIR"

docker run --rm \
  -v "$OUTPUT_DIR":/output \
  "$IMAGE_NAME" \
  bash -c "
    qemu-riscv64 -plugin \$QEMU_PLUGINS/libbbv.so,interval=$INTERVAL,outfile=/output/sha1 \$DHRYSTONE

    simpoint \
      -loadFVFile /output/sha1.0.bb \
      -maxK $MAX_K \
      -saveSimpoints /output/sample.simpoints \
      -saveSimpointWeights /output/sample.weights
  "
