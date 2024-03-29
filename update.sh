#!/bin/bash

docker compose pull

CONTAINER_IMAGE_ID=$(docker compose images -q  | awk '{print "sha256:"$1}')
LATEST_IMAGE_ID=$(docker inspect --format='{{.Id}}' ghcr.io/darwinkel/shepardtts:main)

if [ "$LATEST_IMAGE_ID" != "$CONTAINER_IMAGE_ID" ]
then
    docker compose stop
    docker compose down
    docker compose up -d
    docker image prune -f # Warning: may also remove some of your other old images 
fi
