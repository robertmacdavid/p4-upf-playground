# p4-upf-playground
This repo is for prototyping a 5G User-Plane Function (UPF) written in v1-model p4_16. The prototyping environment is a series of docker images. 
* The bmv2 docker image (built in bmv2img/) hosts a single software BMv2 P4 switch with several virtual interfaces. Python traffic generating scripts in trafficgen/ will generate GTP-U and IP traffic for injecting into the software switch.
* A p4runtime docker image that is used for a naive control plane used to test the validity of the p4 program. The control plane is in p4runtime/ and it will not be production grade.
* An ONOS docker image will be added and used for prototyping a production grade ONOS app used to control the UPF.

The commands required for testing are all present in the Makefile.
1. Build the P4 switch program with `make fabric-build`. If it fails, you may have forgotten to clone the ONOS submodule. 
2. Initialize the containers with `make start`. This will launch the bmv2 switch and static control plane, installing sufficient p4runtime table entries for a simple end-to-end packet test. 
3. Tap into the bmv2 log with `make bmv2-log` to watch packet events in the switch.
4. Create a listener for traffic leaving the switch with either `make recv-gtp` or `make recv-ip`
5. Send traffic into the switch using either `make send-gtp` or `make send-ip`. Send GTP if you're receiving IP (and vice versa) since the switch encapsulates and decapsulates GTP tunnels.

The UPF will be built as an extension to ONOS's fabric.p4, which has been forked and added as a submodule to this repo. The main (fabric.p4) can be found [here](https://github.com/robertmacdavid/onos/tree/master/pipelines/fabric/impl/src/main/resources).
