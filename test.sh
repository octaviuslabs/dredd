#!/bin/bash

export MEM_STORE_HOST=localhost
export MEM_STORE_PORT=6379
export MEM_STORE_DB=0
export MEM_STORE_TYPE=redis
export AWS_ACCESS_KEY_ID=test_placeholder
export AWS_SECRET_ACCESS_KEY=test_placeholder
export Q_TOWATCH=test_placeholder
export QUEUE_ENDPOINT=test_placeholder
export AWS_Q_REGION=test_placeholder
export AWS_S3_BUCKET_NAME=test_placeholder


cd dredd
nosetests
