global multiplicar
section .text

multiplicar:
    push ebp
    mov ebp, esp
    fld dword [ebp + 8]     ; cargar parámetro a
    fld dword [ebp + 12]    ; cargar parámetro b
    fmulp st1, st0          ; a * b
    pop ebp
    ret
