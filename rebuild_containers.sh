#!/bin/bash

docker compose -f application_stack.yaml down

docker rmi local/webapi
docker rmi local/flyway
docker rmi local/pytests
docker rmi local/locust_main
docker rmi local/locust_worker

docker volume prune -f

docker compose -f application_stack.yaml up -d --scale load_worker=6