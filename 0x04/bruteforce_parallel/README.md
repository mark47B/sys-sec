
Параллельный bruteforce-переборщик паролей для zip-архива.

Пространство паролей (`a`-`z`, длина 1-4, итого 475 254 вариантов) делится
на равные чанки между `N` процессами (`multiprocessing.Pool`).
Как только один процесс находит пароль, остальные останавливаются
через разделяемую переменную `Manager().Value`.

---

Запуск:

```bash
python3 bruteforce_parallel.py secret.zip [num_workers]
```

```bash
python3 bruteforce_parallel.py secret.zip 4
Brute-forcing 'secret.zip' with 4 workers...
Password found: pass  (in 6.38s, 4 workers)
```

---
