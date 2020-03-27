#!/usr/bin/env bash

echo "sleeping 1 seconds to wait for bmv2"
sleep 1
echo "done being asleep"

# from the original docker entry point file
source /p4runtime-sh/venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH

python3 /p4runtime/controller.py
echo "controller finished running. entering P4runtime-SH"

/p4runtime-sh/p4runtime-sh --grpc-addr bmv2:50001 \
  --device-id 1 --election-id 0,1
exit 0
