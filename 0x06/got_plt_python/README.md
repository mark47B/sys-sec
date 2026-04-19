Разрешаем attach
```bash
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scopedisassemble main
```

запускаем в терминале 1 test_prog

```bash
./test_prog qwerty42
```

В терминале 2
```bash
$ pgrep -f test_prog 
29785

$ gdb -q
(gdb) attach 29785
Attaching to process 29785
```

Нужно найти функцию puts
```bash
(gdb) disassemble main
...
   0x080491f4 <+94>:    push   %eax
   0x080491f5 <+95>:    call   0x8049050 <puts@plt> # Ссылка на PLT запись для puts
   0x080491fa <+100>:   add    $0x10,%esp
...
```

Находим адрес GOT записи
```bash
(gdb) disassemble 0x8049050
Dump of assembler code for function puts@plt:
   0x08049050 <+0>:     jmp    *0x804c008  # адрес GOT-записи puts
   0x08049056 <+6>:     push   $0x10
   0x0804905b <+11>:    jmp    0x8049020
End of assembler dump.
```

```bash
(gdb) x/1xw 0x804c008
0x804c008 <puts@got.plt>:       0xf492b140 # Реальный адрес puts
```

Смотрим адрес для system, чтобы в дальнейшем заменить puts на него
```bash
(gdb) p system
$1 = {<text variable, no debug info>} 0xf4903430 <system>
```

Подменяем содержимое message
```bash
(gdb) set {char[16]}message = "user/bin/python3"
```

Подменяем ссылку с puts на system
```bash
(gdb) set {int}0x804c008 = 0xf4903430
```

Проверяем, что указатель поменялся
```bash
(gdb) x/1xw 0x804c008
0x804c008 <puts@got.plt>:       0xf4903430
```