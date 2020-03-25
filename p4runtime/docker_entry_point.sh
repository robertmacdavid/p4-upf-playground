#!/usr/bin/env bash

echo "sleeping 5 seconds to wait for mininet"
sleep 5
echo "done being asleep"

# from the original docker entry point file
source /p4runtime-sh/venv/bin/activate

/p4runtime-sh/p4runtime-sh --grpc-addr mininet:50001 \
  --device-id 0 --election-id 0,1 \
  --config /p4build/p4info.txt,/p4build/bmv2.json
exit 0
