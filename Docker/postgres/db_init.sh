#!/bin/sh

set -e

echo "DB INIT ENTRYPOINT STARTING..."

createdb "youtube-analyzer";
