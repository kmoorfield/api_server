#!/bin/bash

docker compose -f application_stack.yaml down

docker rmi local/webapi
docker rmi local/flyway
docker rmi local/pytests

docker volume prune -f

docker compose -f application_stack.yaml up -d