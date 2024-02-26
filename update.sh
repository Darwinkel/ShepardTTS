#!/bin/bash
if ! docker pull ghcr.io/darwinkel/shepardtts:main | grep "Image is up to date for"
then
    docker compose stop
    docker compose down
    docker compose up -d
fi