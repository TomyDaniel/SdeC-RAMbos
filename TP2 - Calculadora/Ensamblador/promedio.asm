global promedio
section .text
section .data
    divisor dd 2.0

promedio:
    push ebp
    mov ebp, esp
    fld dword [ebp + 8]     ; cargar a
    fld dword [ebp + 12]    ; cargar b
    faddp st1, st0          ; a + b
    fld dword [divisor]     ; cargar 2.0
    fdivp st1, st0          ; (a + b) / 2
    pop ebp
    ret
