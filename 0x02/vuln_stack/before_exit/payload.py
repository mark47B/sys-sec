import sys, subprocess

out = subprocess.check_output(['./vuln_stack', 'x'], stderr=subprocess.STDOUT).decode()

buf_addr = [l for l in out.split('\n') if 'buf' in l]
print(f'buf{buf_addr[0]}', file=sys.stderr)
buf_addr = int(buf_addr[0].split()[-1], 16)
print(f'buf{hex(buf_addr)}', file=sys.stderr)
buf_addr -= 112
print(f'correct {hex(buf_addr)}', file=sys.stderr)
