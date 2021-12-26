#!/bin/sh
PORT=3227
PATH="/root/miniature-lighting-desk/crossbar"
cd $PATH
echo "Starting crossbar"

docker run -v  $PWD:/node  -v /etc/letsencrypt:/etc/letsencrypt -u 0 --rm --name=crossbar -it -p $PORT:$PORT --env-file .env crossbario/crossbar
