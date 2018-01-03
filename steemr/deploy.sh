#!/bin/bash

docker build -t steemr .
docker tag steemr furion/steemr
docker push furion/steemr
