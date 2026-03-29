
```bash
 ./vuln_stack ff
addr ␣ buf: ␣ 0x7fffffffcf50 
addr ␣ &v: ␣ 0x7fffffffcf48 
buf: ␣ ff 
```

0x7fffffffcf50 - 0x7fffffffcf48 = 8


```bash
MCS/semestr-4/InfSec/sys-sec/0x02/vuln_stack$ objdump -d -M intel,mnemonic vuln_stack | grep -A 5 '<foo>'
0000000000401176 <foo>:
  401176:       f3 0f 1e fa             endbr64
  40117a:       55                      push   rbp
  40117b:       48 89 e5                mov    rbp,rsp
  40117e:       48 83 c4 80             add    rsp,0xffffffffffffff80
  401182:       48 89 7d 88             mov    QWORD PTR [rbp-0x78],rdi
--
  40121e:       e8 53 ff ff ff          call   401176 <foo>
  401223:       b8 00 00 00 00          mov    eax,0x0
  401228:       c9                      leave
  401229:       c3                      ret
```

0x78 = 120 байт -- размер массива в стеке 
0x7fffffffcf50 -- адрес массива в стеке


```bash
Reading symbols from ./execve_sh...
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
for c in "//bin/sh"]))'
2f 2f 62 69 6e 2f 73 68
```




