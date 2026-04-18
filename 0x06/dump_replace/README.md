1. Запускаем сервер

```bash
python3 server.py &
```

2. Запускаем pyrasite с подменой дампа
```bash
pgrep -f server.py
```

```bash
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope

pyrasite 1569 patch_encrypt.py
```
