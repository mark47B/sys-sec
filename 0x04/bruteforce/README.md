
Последовательный bruteforce-переборщик паролей для zip-архива.

Ограничения: пароль -- строчные буквы `a`-`z`, длина не более 4 символов.
Порядок перебора: `a, b, ..., z, aa, ab, ..., az, ..., za, ..., zz, ..., aaaa, ..., zzzz`

Итого: 26 + 26² + 26³ + 26⁴ = 475 254 вариантов.

---

Создание архива:

```bash
echo "secret content" > secret.txt
zip -P pass secret.zip secret.txt
```

Запуск переборщика:

```bash
python3 bruteforce.py secret.zip
```
