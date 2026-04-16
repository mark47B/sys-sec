section .text
    global _start
_start:
    xor eax, eax
    mov al, 1       ; syscall exit (0x01)
    xor ebx, ebx   ; exit code 0
    int 0x80
