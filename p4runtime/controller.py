import p4runtime_sh.shell as sh
import p4runtime_sh.context as context
import json

sh.setup(
    device_id=1,
    grpc_addr='bmv2:50001',
    election_id=(0, 1), # (high, low)
    config=sh.FwdPipeConfig('/p4build/p4info.txt', '/p4build/bmv2.json')
)
print("successful setup!")

UE   = 0
ENODEB = 1
SPGW = 2
INTERNET = 3
            #  UE,        ENODEB        SPGW       INTERNET
PORTS       = ["1",       "1",          None,      "2"]
NEXT_IDS    = ["1",       "1",          None,      "2"]
IPV4_ADDRS  = ["1.0.0.1", "140.0.0.1", "140.0.0.2", "3.0.0.1"]

TEID = str(0xabcd)
SDF_RULE_ID = "1"
PCC_RULE_ID = "1"

FWD_IPV4_UNICAST = "2"
ETHERTYPE_IPV4 = str(0x0800)
SPGW_DIR_UNKNOWN = "0"
SPGW_DIR_UPLINK = "1"
SPGW_DIR_DOWNLINK = "2"
PCC_GATE_OPEN = "0"
PCC_GATE_CLOSED = "1"

PROTO_UDP = "17"
INNER_UDP_PORT = "44"

filtering_entries = \
        [
            {
                # need rules for every port, because default action is deny
                "table" : "FabricIngress.filtering.ingress_port_vlan",
                "action": "FabricIngress.filtering.permit",
                "keys"  :
                    {
                    "ig_port":port, # exact
                    "vlan_is_valid":"0", # validity, exact
                    },
                "args" : {},
                "priority" : 2
            }
            for port in [PORTS[ENODEB], PORTS[INTERNET]]
        ]+[
            {
                "table" : "FabricIngress.filtering.fwd_classifier",
                "action": "FabricIngress.filtering.set_forwarding_type",
                "keys"  : {
                    "ig_port":port, # exact
                    # per P4RT spec, unset keys->don't care
                    #"hdr.ethernet.dst_addr":("1","0"), # ternary
                    #"hdr.eth_type.value":("1","0"), # ternary
                    "ip_eth_type":ETHERTYPE_IPV4, # exact
                    },
                "args"  : {"fwd_type":FWD_IPV4_UNICAST}, # fwd_type_t
                "priority":2
            }
            for port in [PORTS[ENODEB], PORTS[INTERNET]]
        ]

spgw_entries = \
        [
            {
                "table" : "FabricIngress.spgw_ingress.dl_sess_lookup",
                "action": "FabricIngress.spgw_ingress.set_dl_sess_info",
                "keys"  : {"ipv4_dst":IPV4_ADDRS[UE]},
                "args"  : {"teid":TEID,
                           "s1u_enb_addr":IPV4_ADDRS[ENODEB],
                           "s1u_sgw_addr":IPV4_ADDRS[SPGW]}
            },{
                "table" : "FabricIngress.spgw_ingress.s1u_filter_table",
                "action": "nop",
                "keys"  : {"gtp_ipv4_dst":IPV4_ADDRS[SPGW]},
                "args"  : {}
            },{
                "table" : "FabricIngress.spgw_ingress.sdf_rule_lookup",
                "action": "FabricIngress.spgw_ingress.set_sdf_rule_id",
                "keys"  : {
                            "spgw_direction":SPGW_DIR_UPLINK,
                            "ipv4_src":IPV4_ADDRS[UE], # inner header
                            "ipv4_dst":IPV4_ADDRS[INTERNET],
                            "ip_proto":PROTO_UDP,
                            "l4_sport":INNER_UDP_PORT,
                            "l4_dport":INNER_UDP_PORT,
                          },
                "args"  : {"id":SDF_RULE_ID},
                "priority" : 2
            },{
                "table" : "FabricIngress.spgw_ingress.sdf_rule_lookup",
                "action": "FabricIngress.spgw_ingress.set_sdf_rule_id",
                "keys"  : {
                            "spgw_direction":SPGW_DIR_DOWNLINK,
                            "ipv4_src":IPV4_ADDRS[INTERNET], # inner header
                            "ipv4_dst":IPV4_ADDRS[UE],
                            "ip_proto":PROTO_UDP,
                            "l4_sport":INNER_UDP_PORT,
                            "l4_dport":INNER_UDP_PORT,
                          },
                "args"  : {"id":SDF_RULE_ID},
                "priority" : 2
            },{
                "table" : "FabricIngress.spgw_ingress.pcc_rule_lookup",
                "action": "FabricIngress.spgw_ingress.set_pcc_rule_id",
                "keys"  : {"sdf_rule_id":SDF_RULE_ID},
                "args"  : {"id":PCC_RULE_ID}
            },{
                "table" : "FabricIngress.spgw_ingress.pcc_info_lookup",
                "action": "FabricIngress.spgw_ingress.set_pcc_info",
                "keys"  : {"pcc_rule_id":PCC_RULE_ID},
                "args"  : {"gate_status":PCC_GATE_OPEN}
            }
        ]

forwarding_entries = \
        [
            {
                "table" : "FabricIngress.forwarding.routing_v4",
                "action": "FabricIngress.forwarding.set_next_id_routing_v4",
                # inner IP header
                "keys"  : {"ipv4_dst":IPV4_ADDRS[idx] + "/32"},
                "args"  : {"next_id":NEXT_IDS[idx]}
            }
            for idx in [UE, INTERNET]
        ]

acl_entries = [] # default nop/allow is fine


next_entries = \
        [
            {
                "table" : "FabricIngress.next.simple",
                "action": "FabricIngress.next.output_simple",
                "keys"  : {"next_id" : NEXT_IDS[idx]},
                "args"  : {"port_num" : PORTS[idx]}
            }
            for idx in [UE, INTERNET]
        ]

entries =   filtering_entries + \
            spgw_entries + \
            forwarding_entries + \
            acl_entries + \
            next_entries + \
            []

print("deleting entries from any previous run")


tables = sh.P4Objects(context.P4Type.table)
count = 0
for table in tables:
    for te in sh.TableEntry(table.name).read():
        count += 1
        te.delete()
print("Deleted %d entries" % count)


print("installing entries")
for i, entry in enumerate(entries):
    print("installing %d" % i)
    try:
        te = sh.TableEntry(entry["table"])(action=entry["action"])
        for key, val in entry["keys"].items():  te.match[key] = val
        for arg,val in entry["args"].items():   te.action[arg] = val
        priority = entry.get("priority", None)
        if priority != None: te.priority = priority
        te.insert()
    except Exception:
        print("ENTRY FAILED:\n", json.dumps(entry, indent=2), "\nEND FAILURE")
        raise Exception


sh.teardown()
print("Successful teardown!")
