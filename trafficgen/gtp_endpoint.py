#!/usr/bin/python3

from scapy.contrib import gtp
from scapy.all import sendp, sniff, Ether, IP, UDP
import sys

GTP_PORT = 2152
OUT_IFACE = 'veth1'
OUT_MAC = 'ce:b9:04:59:7e:37'
def send_gtp():
    pkt = Ether(dst=OUT_MAC) / \
            IP(dst='192.168.0.1') / \
            UDP(dport=GTP_PORT) / \
            gtp.GTPHeader(version=1, PT=0, E=0, S=0, PN=0, gtp_type=0xff) / \
            IP() / \
            UDP() / \
            "Hello!"

    print("Sending 1 GTP packet to interface", OUT_IFACE)
    sendp(pkt, iface=OUT_IFACE)
    print("Done.")

def sniff_gtp():
    sniff(iface=OUT_IFACE, prn=lambda x:x.show, filter="udp port %d" % GTP_PORT, count=1)

if __name__ == "__main__":
    usage = "usage: %s <send|recv>" % sys.argv[0]
    if len(sys.argv) < 2:
        print(usage)
        exit(1)
    if sys.argv[1] == "send":
        send_gtp()
    elif sys.argv[1] == "recv":
        sniff_gtp()
    else:
        print(usage)
        exit(1)

