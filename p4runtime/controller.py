import p4runtime_sh.shell as sh

sh.setup(
    device_id=1,
    grpc_addr='mininet:50001',
    election_id=(0, 1), # (high, low)
    config=sh.FwdPipeConfig('/p4build/p4info.txt', '/p4build/bmv2.json')
)

print("successful setup!")

sh.teardown()

print("Successful teardown!")
