#!/bin/sh
PORT=3227
echo "Starting crossbar"

docker run -v  $PWD:/node  -v /etc/letsencrypt:/etc/letsencrypt -u 0 --rm --name=crossbar -it -p $PORT:$PORT --env-file .env crossbario/crossbar
