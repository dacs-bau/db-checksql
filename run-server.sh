#!/bin/sh

PATH=/micromamba/bin:$PATH
export PATH

cd /app
exec /micromamba/bin/python -m uvicorn \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --ws none \
    --no-use-colors \
    api-server:app
