#!/bin/sh

PORT=3227
TICKET=$(cat .crossbar-ticket)

echo "Starting crossbar"

CROSSBAR_TICKET=TICKET docker run -v  $PWD:/node  -v /etc/letsencrypt:/etc/letsencrypt -u 0 --rm --name=crossbar -it -p $PORT:$PORT crossbario/crossbar
