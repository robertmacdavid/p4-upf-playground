FROM opennetworking/mn-stratum

# build from source to get access to the contrib submodule which contains GTP
ENV BUILD_DEPS \
    git \
    python3-pip \
    python3-setuptools \
    python3

RUN apt-get update && \
    apt-get install -y --no-install-recommends ${BUILD_DEPS}

RUN git config --global http.sslVerify false && \
    git clone https://github.com/secdev/scapy.git && \
    cd scapy && \
    python3 setup.py install --user && \
    cd
