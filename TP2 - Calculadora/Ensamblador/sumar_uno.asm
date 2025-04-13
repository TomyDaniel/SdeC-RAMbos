global sumar_uno
section .text

sumar_uno:
    push ebp
    mov ebp, esp
    fld dword [ebp + 8]     ; cargar parámetro float desde stack
    fld1                    ; cargar 1.0
    faddp st1, st0          ; sumar y dejar en st(0)
    pop ebp
    ret
