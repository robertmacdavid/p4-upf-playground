import p4runtime_sh.shell as sh

sh.setup(
    device_id=1,
    grpc_addr='bmv2:50001',
    election_id=(0, 1), # (high, low)
    config=sh.FwdPipeConfig('/p4build/p4info.txt', '/p4build/bmv2.json')
)
print("successful setup!")


# te = table_entry['MyIngress.ipv4_lpm'](action='MyIngress.ipv4_forward')
te = sh.TableEntry('MyIngress.ipv4_lpm')(action='MyIngress.ipv4_forward')
te.match['hdr.ipv4.dstAddr'] = '192.168.0.1'
te.action['dstAddr'] = 'd2:61:9e:d1:0f:1c'
te.action['port'] = "1"
te.insert()



sh.teardown()
print("Successful teardown!")
