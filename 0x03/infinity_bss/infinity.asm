section .text
    global _start
_start:
    jmp $   ; eb fe -- бесконечный цикл (jmp -2, прыжок на себя)
