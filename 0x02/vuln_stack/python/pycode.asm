section .text
    global _start
_start:
    xor eax , eax
    push eax
    push 0x336e6f68   ; "hon3"
    push 0x7479702f   ; "/pyt"
    push 0x6e69622f   ; "/bin"
    push 0x7273752f   ; "/usr"
    mov ebx, esp
    mov ecx, eax
    mov edx, eax
    mov al, 0xb
    int 0x80