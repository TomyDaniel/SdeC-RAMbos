global dividir
section .text

dividir:
    push ebp
    mov ebp, esp
    fld dword [ebp + 8]     ; cargar a
    fld dword [ebp + 12]    ; cargar b
    fdivp st1, st0          ; a / b
    pop ebp
    ret
