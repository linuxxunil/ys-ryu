#!/bin/sh
curl -X POST -d '{"address": "192.168.1.1/24"}' http://localhost:8081/router/0000000000000001
curl -X POST -d '{"address": "192.168.2.1/24"}' http://localhost:8081/router/0000000000000001
curl -X POST -d '{"address": "192.168.3.1/24"}' http://localhost:8081/router/0000000000000001
curl -X POST -d '{"address": "192.168.4.1/24"}' http://localhost:8081/router/0000000000000001
