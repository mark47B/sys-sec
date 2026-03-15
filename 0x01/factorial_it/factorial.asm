section .data
    prompt     db "Введите число n (0–20): ", 0
    fmt_in     db "%lld", 0
    fmt_out    db "Факториал = %lld", 10, 0

section .bss
    n          resq 1

section .text
    global main
    extern printf
    extern scanf

main:
    push rbp
    mov  rbp, rsp

    lea  rdi, [prompt]
    xor  rax, rax
    call printf

    lea  rdi, [fmt_in]
    lea  rsi, [n]
    xor  rax, rax
    call scanf

    mov  rcx, [n]
    mov  rax, 1

    cmp  rcx, 1
    jbe  .print_result

.loop:
    imul rax, rcx
    dec  rcx
    cmp  rcx, 1
    ja   .loop

.print_result:
    lea  rdi, [fmt_out]
    mov  rsi, rax
    xor  rax, rax
    call printf

    xor  rax, rax
    leave
    ret