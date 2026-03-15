section .data
    prompt     db "Введите число n (0-20): ", 0
    input_fmt  db "%lld", 0
    output_fmt db "Факториал n! = %lld", 10, 0

section .bss
    number     resq 1

section .text
    global main
    extern printf
    extern scanf

main:
    push rbp
    mov  rbp, rsp

    lea  rdi, [prompt]
    call printf

    lea  rdi, [input_fmt]
    lea  rsi, [number]
    call scanf

    mov  rdi, [number]
    call factorial

    lea  rdi, [output_fmt]
    mov  rsi, rax
    call printf

    mov  rax, 0
    pop  rbp
    ret

factorial:
    push rbp
    mov  rbp, rsp

    cmp  rdi, 1
    jle  .base_case

    ; --- Рекурсия ---
    push rdi
    dec  rdi
    call factorial

    pop  rdi
    imul rax, rdi

    jmp  .end

.base_case:
    mov  rax, 1

.end:
    pop  rbp
    ret