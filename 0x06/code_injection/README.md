```bash
cat /proc/$(pgrep simple_loop)/maps | grep rwx
```
RWX-страниц в адресном пространстве нет. Значит подключимся к процессу через gdb, вызовем
 `mmap()` прямо из gdb -> выделим RWX-страницу; запишем shellcode в эту страницу 
 и вызовем его

attach к уже запущенному процессу 

build and run (в терминале 1)
```bash
gcc -o simple_loop simple_loop.c
./simple_loop
```

Терминал 2
```bash
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope

python3 inject_python.py $(pgrep simple_loop)
gdb -q --batch -x inject.gdb
```

Фактически, всё, что генерирует inject_python можно и ручками ввести.
Что внутри генерируемого файла: 1. attach к процессу 2. Выделение rwx памяти 3. складывание
shellcode в эту память 4. вызов
