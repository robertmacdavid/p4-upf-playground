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

send-gtp:
	docker-compose exec bmv2 /trafficgen/gtp_endpoint.py send

recv-gtp:
	docker-compose exec bmv2 /trafficgen/gtp_endpoint.py recv
