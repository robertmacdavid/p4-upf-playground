# p4-upf-playground
This repo is for prototyping a 5G User-Plane Function (UPF) written in v1-model p4_16. The prototyping environment is a series of docker images. 
* The bmv2 docker image (built in bmv2img/) hosts a single software BMv2 P4 switch with several virtual interfaces. Python traffic generating scripts in trafficgen/ will generate GTP-U and IP traffic for injecting into the software switch.
* A p4runtime docker image that is used for a naive control plane used to test the validity of the p4 program. The control plane is in p4runtime/ and it will not be production grade.
* An ONOS docker image will be added and used for prototyping a production grade ONOS app used to control the UPF.

The UPF will be built as an extension to ONOS's fabric.p4, which has been forked and added as a submodule to this repo. The main (fabric.p4) can be found [here](https://github.com/robertmacdavid/onos/tree/master/pipelines/fabric/impl/src/main/resources).
