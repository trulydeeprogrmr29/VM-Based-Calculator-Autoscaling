#!/bin/bash

SERVER="http://192.168.122.3:5000"
REQUESTS=${1:-5}

if ! [[ "$REQUESTS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: ./run.sh <number_of_requests>"
    exit 1
fi

echo "Sending $REQUESTS requests to Server VM..."

for ((i=1; i<=REQUESTS; i++))
do
    RESPONSE=$(curl -s -X POST "$SERVER/calculate" \
        -H "Content-Type: application/json" \
        -d '{"a":10,"b":5,"operation":"add"}')

    echo "Request $i: $RESPONSE"
done

echo "Completed $REQUESTS requests."
