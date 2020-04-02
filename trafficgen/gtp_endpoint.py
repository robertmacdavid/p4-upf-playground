#!/usr/bin/python3

from scapy.contrib import gtp
from scapy.all import sendp, sniff, Ether, IP, UDP
import sys


UE   = 0
ENODEB = 1
SPGW = 2
INTERNET = 3
            #  UE,        ENODEB     SPGW       INTERNET
PORTS       = ["1",       "1",       None,      "2"]
NEXT_IDS    = ["1",       "1",       None,      "2"]
IPV4_ADDRS  = ["1.0.0.1", "140.0.0.1", "140.0.0.2", "3.0.0.1"]
IFACES      = ["veth1",   "veth1",      None,      "veth3"]

TEID = str(0xabcd)

INNER_UDP_PORT = 44


GTP_PORT = 2152
OUT_MAC = 'ce:b9:04:59:7e:37'
def send_gtp():
    pkt = Ether(dst=OUT_MAC) / \
            IP( src=IPV4_ADDRS[ENODEB],
                dst=IPV4_ADDRS[SPGW]) / \
            UDP(dport=GTP_PORT) / \
            gtp.GTPHeader(version=1, PT=0, E=0, S=0, PN=0, gtp_type=0xff) / \
            IP( src=IPV4_ADDRS[UE],
                dst=IPV4_ADDRS[INTERNET]) / \
            UDP(sport=INNER_UDP_PORT,
                dport=INNER_UDP_PORT) / \
            "Hello!"

    iface = IFACES[ENODEB]
    print("Sending the following packet to interface %s:" % iface)
    pkt.show2()
    sendp(pkt, iface=iface)
    print("Done.")


def send_ip():
    pkt = Ether(dst=OUT_MAC) / \
            IP(src=IPV4_ADDRS[INTERNET],
                    dst=IPV4_ADDRS[UE]) / \
            UDP(sport=INNER_UDP_PORT,
                    dport=INNER_UDP_PORT) / \
            "Hello!"

    iface = IFACES[INTERNET]
    print("Sending the following packet to interface %s:" % iface)
    pkt.show2()
    sendp(pkt, iface=iface)
    print("Done.")


def sniff_gtp():
    sniff(iface=IFACES[ENODEB], prn=lambda x:x.show2, filter="udp port %d" % GTP_PORT, count=1)

def sniff_ip():
    sniff(iface=IFACES[INTERNET], prn=lambda x:x.show2, filter="ip", count=1)


if __name__ == "__main__":
    usage = "usage: %s <send|recv> <gtp|ip>" % sys.argv[0]
    if len(sys.argv) != 3:
        print(usage)
        exit(1)

    arg_pair = (sys.argv[1], sys.argv[2])
    funcs = {("send", "gtp") : send_gtp,
             ("recv", "gtp") : sniff_gtp,
             ("send", "ip")  : send_ip,
             ("recv", "ip")  : sniff_ip}

    if arg_pair not in funcs:
        print(usage)
        exit(1)

    funcs[arg_pair]()

