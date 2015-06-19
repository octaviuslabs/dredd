#!/bin/bash

export MEM_STORE_HOST=localhost
export MEM_STORE_PORT=6379
export MEM_STORE_DB=0
export MEM_STORE_TYPE=redis

cd dredd
nosetests
