# Run

```bash
sudo apt install nasm -y
```

Собираем объектный файл
```bash
nasm -f elf64 factorial.asm -o factorial.o
```

Линкуем с библиотекой C отключаем pie(Position Independent Executable), так как используем абсолютные адреса внутри.
```bash
gcc -no-pie factorial.o -o factorial
```

Даём права на запуск
```bash
chmod +x factorial
```

```bash
./factorial
```

# Result
```bash
$ chmod +x factorial
$ ./factorial 
Введите число n (0–20): 0
Факториал = 1
$ ./factorial 
Введите число n (0–20): 19
Факториал = 121645100408832000
$ ./factorial
Введите число n (0–20): 20
Факториал = 2432902008176640000
$ ./factorial 
Введите число n (0–20): 21
Факториал = -4249290049419214848
```