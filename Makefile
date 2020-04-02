endpoint-run := docker-compose exec bmv2 /trafficgen/gtp_endpoint.py

bmv2-log:
	docker-compose exec bmv2 tail -f stratum_bmv2.log

start:
	docker-compose up -d

stop:
	docker-compose stop

p4rt-sh:
	docker attach --detach-keys "ctrl-d" p4runtime

p4-build:
	./p4-build.sh p4src/basic.p4

fabric-build:
	./p4-build.sh onos/pipelines/fabric/impl/src/main/resources/fabric.p4 "-DWITH_SPGW -DWITH_SIMPLE_NEXT -DCPU_PORT=255 -DWITH_SPGW_PCC_GATING"

send-gtp:
	${endpoint-run} send gtp

recv-gtp:
	${endpoint-run} recv gtp

send-ip:
	${endpoint-run} send ip

recv-ip:
	${endpoint-run} recv ip

